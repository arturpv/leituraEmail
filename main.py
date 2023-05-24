import email
import imaplib
import re
import time

def leituraImap():
    imap_server = 'imap.gmail.com'
    imap_port = 993
    imap_username = 'seu_email@gmail.com'
    imap_password  = 'sua_senha'

    #Conecta ao servidor IMAP
    imap = imaplib.IMAP4_SSL(imap_server, imap_port)

    #Faz login na conta de email
    imap.login(imap_username, imap_password)

    #Seleciona a caixa de entrada
    imap.select('INBOX')

    contador = 0

    while contador < 4:
        #Procura emails não lidos com o assunto específico
        status, messages = imap.search(None, 'SUBJECT "assunto do email"')

        if status == 'OK':
            email_ids = messages[0].split()

            if email_ids:
                #Obtem o ID do último e-mail encontrado
                latest_email_id = email_ids[-1]

                #Busca o e-mail completo pelo ID
                status, email_data = imap.fetch(latest_email_id, '(RFC822)')

                if status == 'OK':
                    #Analisa os dados do e-mail
                    raw_email = email_data[0][1]
                    email_message = email.message_from_bytes(raw_email)

                    #Extrai o código percorrendo as partes do e-mail
                    verification_code = extract_verification_code(email_message)

                    if verification_code:
                        print("Código de verificação:", verification_code)
                        break
        contador +=1
        if contador < 4:
            print("E-mail não encontrado. Tentando novamente em 10 segundos...")
            time.sleep(10)

    if contador >= 4:
        print("Nenhum e-mail com o assunto 'assunto do email' encontrado.")
    #Fecha a conexão com o servidor IMAP
    imap.logout()

def extract_verification_code(part):
    if part.get_content_type() == 'text/plain':
        pattern = r'[A-Z0-9]{6}'
        match = re.search(pattern, part.get_payload())
        if match:
            return match.group(0)
    elif part.is_multipart():
        for subpart in part.get_payload():
            result = extract_verification_code(subpart)
            if result:
                return result

def main():
    leituraImap()

if __name__ == '__main__':
    main()
