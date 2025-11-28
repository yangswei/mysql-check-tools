import os
import subprocess
import platform
import re
import sys

class dopEnvcheck:
    def __init__(self):
        pass
        
    def run_command(self, cmd):
        """执行命令并返回输出"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error: {e}"
    
    def get_system_info(self):
        """获取系统版本信息"""
        system_info = {}
        
        # 系统类型
        system_info['system'] = 'Linux'
        
        # 尝试读取/etc/os-release文件
        try:
            with open('/etc/os-release', 'r') as f:
                os_release = f.read()
                
            # 提取系统名称
            name_match = re.search(r'NAME="([^"]+)"', os_release)
            if name_match:
                system_info['name'] = name_match.group(1)
            
            # 提取版本号
            version_match = re.search(r'VERSION="([^"]+)"', os_release)
            if version_match:
                system_info['version'] = version_match.group(1)
            else:
                # 尝试获取版本ID
                version_id_match = re.search(r'VERSION_ID="([^"]+)"', os_release)
                if version_id_match:
                    system_info['version'] = version_id_match.group(1)
            
            # 提取PRETTY_NAME
            pretty_name_match = re.search(r'PRETTY_NAME="([^"]+)"', os_release)
            if pretty_name_match:
                system_info['pretty_name'] = pretty_name_match.group(1)
                
        except Exception as e:
            system_info['error'] = f"无法读取系统版本信息: {e}"
        
        # 如果无法从os-release获取，尝试其他方法
        if 'name' not in system_info:
            try:
                # 尝试麒麟系统
                if os.path.exists('/etc/kylin-release'):
                    result = self.run_command("cat /etc/kylin-release")
                    if "Error" not in result:
                        system_info['name'] = "Kylin Linux"
                        system_info['version'] = result.strip()
                # 尝试Red Hat系
                elif os.path.exists('/etc/redhat-release'):
                    result = self.run_command("cat /etc/redhat-release")
                    if "Error" not in result:
                        system_info['name'] = "Red Hat/CentOS"
                        system_info['version'] = result.strip()
                # 尝试Debian系
                elif os.path.exists('/etc/issue.net'):
                    result = self.run_command("cat /etc/issue.net")
                    if "Error" not in result:
                        system_info['name'] = "Debian/Ubuntu"
                        system_info['version'] = result.strip()
                else:
                    system_info['name'] = "Unknown Linux Distribution"
            except:
                system_info['name'] = "Unknown Linux Distribution"
        
        return system_info
    
    def get_disk_mount_info(self):
        """获取磁盘挂载情况"""
        disk_info = []
        
        try:
            # 使用df命令获取挂载信息，排除虚拟文件系统
            result = self.run_command("df -h | grep -E '^/dev/(vd|sd|nvme|hd|xvd)'")
            if "Error" in result:
                return [{"error": "无法获取磁盘挂载信息"}]
            
            lines = result.split('\n')
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 6:
                        disk = {
                            'filesystem': parts[0],
                            'total': parts[1],
                            'used': parts[2],
                            'free': parts[3],
                            'usage_percent': parts[4],
                            'mount_point': parts[5]
                        }
                        disk_info.append(disk)
        
        except Exception as e:
            disk_info.append({"error": f"获取磁盘信息时出错: {e}"})
        
        return disk_info
    
    def get_memory_info(self):
        """获取内存信息"""
        memory_info = {}
        
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
                
            # 提取内存信息
            mem_total_match = re.search(r'MemTotal:\s+(\d+)\s+kB', meminfo)
            mem_available_match = re.search(r'MemAvailable:\s+(\d+)\s+kB', meminfo)
            mem_free_match = re.search(r'MemFree:\s+(\d+)\s+kB', meminfo)
            
            if mem_total_match:
                total_kb = int(mem_total_match.group(1))
                memory_info['total'] = f"{total_kb / 1024 / 1024:.2f} GB"
                
            if mem_available_match:
                available_kb = int(mem_available_match.group(1))
                memory_info['available'] = f"{available_kb / 1024 / 1024:.2f} GB"
                if mem_total_match:
                    usage_percent = (1 - available_kb / total_kb) * 100
                    memory_info['usage_percent'] = f"{usage_percent:.1f}%"
            elif mem_free_match:
                free_kb = int(mem_free_match.group(1))
                memory_info['free'] = f"{free_kb / 1024 / 1024:.2f} GB"
                if mem_total_match:
                    usage_percent = (1 - free_kb / total_kb) * 100
                    memory_info['usage_percent'] = f"{usage_percent:.1f}%"
                    
        except Exception as e:
            memory_info['error'] = f"无法获取内存信息: {e}"
        
        return memory_info
    
    def get_cpu_info(self):
        """获取CPU信息"""
        cpu_info = {}
        
        try:
            # 逻辑核心数
            cpu_info['logical_cores'] = os.cpu_count()
            
            # 获取CPU指令集信息
            with open('/proc/cpuinfo', 'r') as f:
                content = f.read()
                
            # 检查AVX2
            cpu_info['avx2'] = 'avx2' in content.lower()
            # 检查BMI2
            cpu_info['bmi2'] = 'bmi2' in content.lower()
            
            # 获取CPU型号
            model_match = re.search(r'model name\s*:\s*(.+)', content)
            if model_match:
                cpu_info['model'] = model_match.group(1).strip()
                
        except Exception as e:
            cpu_info['error'] = f"无法获取CPU信息: {e}"
        
        return cpu_info
    
    def get_kernel_version(self):
        """获取内核版本"""
        return platform.release()
    
    def get_gpu_info(self):
        """获取GPU信息"""
        gpu_info = {}
        
        try:
            # 尝试使用nvidia-smi
            result = self.run_command("which nvidia-smi")
            if "Error" not in result and result:
                nvidia_result = self.run_command("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader")
                if "Error" not in nvidia_result and nvidia_result:
                    gpu_list = []
                    for line in nvidia_result.split('\n'):
                        if line.strip():
                            parts = line.split(',')
                            if len(parts) >= 2:
                                gpu_list.append(f"{parts[0].strip()} ({parts[1].strip()})")
                            else:
                                gpu_list.append(line.strip())
                    gpu_info['nvidia'] = gpu_list
            
            # 如果没有检测到NVIDIA GPU，尝试使用lspci检测其他GPU
            if not gpu_info:
                result = self.run_command("which lspci")
                if "Error" not in result and result:
                    pci_result = self.run_command("lspci | grep -i vga")
                    if "Error" not in pci_result and pci_result:
                        gpu_list = [line.strip() for line in pci_result.split('\n') if line.strip()]
                        if gpu_list:
                            gpu_info['other'] = gpu_list
        
        except Exception as e:
            gpu_info['error'] = f"无法获取GPU信息: {e}"
        
        return gpu_info