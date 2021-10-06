from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint, choice
import os
from selenium.webdriver.common.action_chains import ActionChains
import getpass

login = str(input("Insira o login: ")).strip()
sleep(0.5)

#tratativa de login não inserido
while login == "":
    print("Login não preenchido. Por favor insira o login.")
    sleep(0.5)
    login = input("Login: ").strip()
    if login != "":
        break
    else:
        continue
    sleep(0.5)

senha = getpass.getpass("Insira a senha: ").strip()
sleep(0.5)

#tratativa de senha não inserida
while senha == "" or len(senha) < 6:
    print("Senha não preenchida ou menor que 6 caracteres. Por favor insira novamente")
    sleep(0.5)
    senha = getpass.getpass("Senha: ").strip()
    sleep(0.5)
    if senha != "" and len(senha) >= 6:
        break
    else:
        continue


link = str(input("insira a url do sorteio do instagram aqui: ")).strip()
sleep(0.5)

#trativa de link não inserido ou link que não seja do insta
try: 
    while link == "" or "https://www.instagram.com/p/" not in link:
        link = input("URL não é do domínio do instagram ou não foi inserida. Por favor insira o url: ").strip()
        if link != "" and link == "https://www.instagram.com/p/" not in link:
            sleep(0.5)
            break
        else:
            continue
except:
    pass

while True:
    try:
        amount_comments = int(input("Quantos comentários deseja  inserir (recomendado acima de 5, máximo 20): "))
        amount_comments_array = []
        if amount_comments < 5 or  amount_comments > 20:
            sleep(0.5)
            raise ValueError("Quantidade inválida, por favor insira um número de 1 a 20\n")
            #tratativa de válor diferente de int
    except ValueError as e:
        print("Valor inválido: ", e)
    else:
        break

for i in range(0, amount_comments):
    commentsfor = str(input(f"{1+i}° Comentário: "))
    while commentsfor == "":
        commentsfor = str(input(f"Por favor insira o {1+i}° comentário para prosseguir: "))
        if commentsfor != "":
            break
        else:
            continue
    amount_comments_array.append(commentsfor)    
    sleep(0.5)

#Parei aqui, a ideia é fazer um array com o tamanho do número que o usuário inserir nos comentários  e fazer ele preencher com comentários x vezes o número que preencheu. OK.
            

driver = webdriver.Firefox() #entra na pasta onde está  o geckodriver e executa
driver.get("https://www.instagram.com/") #pegar o url do insta ou de qualquer site que quisermos
sleep(0.5)
driver.find_element_by_xpath(r'//input[@aria-label="Telefone, nome de usuário ou email"]').send_keys(login)
sleep(0.5)
driver.find_element_by_xpath(r'//input[@aria-label="Senha"]').send_keys(senha)
sleep(0.5)
driver.find_element_by_xpath(r'//*[@id="loginForm"]/div/div[3]/button').click()
sleep(0.5)

#tratativa de erro de login ou senha
try:
    sleep(0.5)
    errorAlert = driver.find_element_by_id("slfErrorAlert")
    sleep(0.5)
    while errorAlert:
        driver.refresh()
        print("Senha ou login inválidos. Por favor insira-os novamente. ")
        login = input("\nInsira o login: ").strip()
        senha = getpass.getpass("\nInsira a senha: ").strip()
        driver.find_element_by_xpath(r'//input[@aria-label="Telefone, nome de usuário ou email"]').send_keys(login)
        sleep(0.5)
        driver.find_element_by_xpath(r'//input[@aria-label="Senha"]').send_keys(senha)
        sleep(0.5)
        driver.find_element_by_xpath(r'//*[@id="loginForm"]/div/div[3]/button').click()
        sleep(0.5)
        if driver.find_element_by_id("slfErrorAlert"):
            continue 
        else:
            break
except:
    pass
sleep(2)
driver.get(link) #Link do sorteio aqui
sleep(2)

#tratativa de link de sorteio inválido
try:
    errorLink = driver.find_element_by_xpath('//html/body/div[1]/section/main/div/div/h2')
    sleep(0.5)
    while errorLink:
        print("O link inserido não existe, tente novamente.")
        link = input("insira novamente a url do sorteio aqui: ").strip()
        sleep(0.5)
        driver.get(link)
        sleep(0.5)
        if driver.find_element_by_xpath('//html/body/div[1]/section/main/div/div/h2'):
            continue
        else:
            break
except:
    pass

class comment(object):
    @staticmethod
    def digitar(frase, digitar):
        for letra in frase:
            digitar.send_keys(letra)
            sleep(randint(1,5)/30)

def comentarios():
    comments = 0
    error = 0
    while True:
        #comments_list =  randint(1, amount_comments_array)
        textarea = driver.find_element_by_class_name('Ypffh')
        sleep(0.5)
        textarea.click()
        sleep(0.5)
        textarea2 = driver.find_element_by_xpath('//textarea[@placeholder="Adicione um comentário..."]')
        sleep(randint(2,5))
        comment.digitar(choice(amount_comments_array), textarea2)
        #criar input para perguntar de quanto em quanto tempo o usuário deseja que o bot comente
        sleep(randint(3,7))#90,500
        driver.find_element_by_xpath('//button[text()="Publicar"]').click()
        sleep(0.5)
        comments += 1
        sleep(0.5)
        print(f"Comentários enviados: {comments}")
        sleep(0.5)
        #Tratamento de disabled
        try:
            pass
        except:
            sleep(0.5)
            driver.find_element_by_xpath('//button[@disabled]')
            driver.refresh()
            print('refresh por disabled')
            
        
        #tratamento de timeout
        
        try:
            sleep(2)
            driver.find_element_by_class_name('gxNyb')
            driver.refresh()
            error += 1
            
        except:
            if(error > 0):
                error -= 1
        if(error == 3):
            sleep(21.600) #6 horas de timeout para depois rodar o código novamente
            error = 0
    
comentarios()

#Este bot tem limite de 11 horas de execução, depois disso o insta pede para alterar a senha da acc por ações suspeitas