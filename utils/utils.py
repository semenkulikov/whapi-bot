def send_message_to_whatsapp(greenAPI, group_id, message):
    """
    Отправляет сообщение через WhatsApp API
    """
    result = greenAPI.sending.sendMessage(group_id, message)
    return result


def send_document_to_whatsapp(greenAPI, group_id, path_to_file, filename, message):
    """
    Отправляет документ через WhatsApp API
    greenAPI: объект greenAPI
    group_id: идентификатор группы
    path_to_file: путь до файла
    filename: имя файла
    message: сообщение-справка
    """
    result = greenAPI.sending.sendFileByUpload(group_id, path_to_file, filename, message)
    return result
