from app.utils.icafeApi import icafeApi


def createIcafe():
    projectCode = "projectCode"
    projectName = "projectName"
    title = "title"
    api = icafeApi()
    api.create(projectCode, projectName, title)