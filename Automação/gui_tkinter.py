# Importar bibliotecas responsáveis pela navegação web e interface gráfica.
from tkinter import *
from tkinter import messagebox
from navigations import WBrowser, WWaits
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class Screens:

    def __init__(self):
        self.window = Tk()
        self.resultado = None
        self.username = None
        self.password = None
        self.driver = None

        # Images
        self.logo_sicredi = PhotoImage(file=r'assets\img\logo_sicredi.gif')
        self.linha = PhotoImage(file=r'assets\img\linha_screens.png')
        self.btn_ok = PhotoImage(file=r'assets\img\btn_ok.png')

    def login(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()
        
        # Fecha a janela após capturar os dados
        self.window.destroy()
        
        # Chama a função abrir_portal para tentar o login no portal
        self.abrir_portal()

    def btn_sim_click(self):
        self.resultado = True
        self.window.destroy()

    def final(self, titulo, subtitulo):
        
        if self.resultado is None:
            window = self.window
            logo_sicredi = self.logo_sicredi
            linha = self.linha
        else: 
            window = Tk()
            logo_sicredi = PhotoImage(file=r'assets\img\logo_sicredi.gif')
            linha = PhotoImage(file=r'assets\img\linha_screens.png')

        # Config
        window.title("Conciliação de Consignados")
        window.maxsize(700, 600) #tamanho max / width x height
        window.geometry('700x600')#tamanho / width x height
        window.config(padx=10, pady=50, bg='white')

        # Labels
        Label(window,
            image=logo_sicredi, 
            bg='white',
            pady=20).pack()
        Label(window, 
            text="Conciliação de Consignados",
            font="Aptos 21 bold", 
            bg='white',
            pady=25).pack()
        Label(window,
            image=linha, 
            bg='white',
            pady=20).pack()
        Label(window,
            text='',
            bg='white',
            pady=10).pack()
        Label(window,
            text='', 
            bg='white',
            pady=5).pack()
        Label(window, 
            text=f"{titulo}",
            font=f"Aptos 17 bold", 
            bg='white',
            pady=20).pack()
        Label(window, 
            text=f"{subtitulo}",
            font=f"Aptos 15", 
            bg='white',
            pady=20).pack()
        Label(window,
            text='',
            bg='white',
            pady=10).pack()
        Label(window,
            image=linha, 
            bg='white',
            pady=30).pack()
        Label(window,
            text='',
            bg='white',
            pady=10).pack()

    def confirmacao(self):

        window = self.window

        # Config
        window.title("Conciliação de Consignados")
        window.maxsize(700, 600) #tamanho max / width x height
        window.geometry('700x600')#tamanho / width x height
        window.config(padx=10, pady=50, bg='white')

        # Images
        logo_sicredi = self.logo_sicredi
        linha = self.linha
        btn_ok = self.btn_ok

        # Labels
        Label(window,
            image=logo_sicredi, 
            bg='white',
            pady=20).pack()
        Label(window, 
            text="Conciliação de Consignados",
            font="Aptos 21 bold", 
            bg='white',
            pady=25).pack()
        Label(window,
            image=linha, 
            bg='white',
            pady=20).pack()
        
        # Frame para organizar os campos de entrada lado a lado
        frame_login = Frame(window, bg='white')
        frame_login.pack(pady=10)

        Label(frame_login, text="Username:", bg='white').pack(side=LEFT, padx=5)
        self.entry_username = Entry(frame_login)
        self.entry_username.pack(side=LEFT, padx=5)

        Label(frame_login, text="Password:", bg='white').pack(side=LEFT, padx=5)
        self.entry_password = Entry(frame_login, show="*")
        self.entry_password.pack(side=LEFT, padx=5)

        # Botão de login
        btn_login = Button(window, text='Login', command=self.login, bd=0, bg='white', padx='5')
        btn_login.config(image=btn_ok)
        btn_login.pack(pady=20)

        window.mainloop()
        
    # Abre o fluid para validar o usuário e senha informados pelo usuário.
    def abrir_portal(self):
        self.driver = WBrowser.chrome_browser('https://portalconsignado', headless=False,maximized=True)
        self.driver.execute_script("document.body.style.zoom='80%'")
        print('Verificando Login...')
        
        # Espera aparecer "Entrar"
        WWaits.clickable(self.driver, By.XPATH, '//*[@id="btnSubmit"]', 25).click()
    
        # Informa Usuário informado no Main
        WWaits.clickable(self.driver, By.XPATH, '//*[@id="fieldUser"]', 25).send_keys(self.username)
    
        # Informa Senha informada no Main
        WWaits.clickable(self.driver, By.XPATH, '//*[@id="fieldPassword"]', 25).send_keys(self.password)
        
        # Informa Senha informada no Main
        WWaits.clickable(self.driver, By.XPATH, '//*[@id="btnSubmit"]', 25).click()
        
        # Verifica se o login foi bem-sucedido
        try:
            WWaits.visible(self.driver, By.XPATH, '/html/body/app-root/app-topo/nav/nav/a', 10)
            print('Login e Senha corretos.')
        except:
            messagebox.showerror("Login Info", "Nome de usuário ou senha incorretos.")
            print('Login e Senha incorretos!')