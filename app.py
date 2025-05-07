import customtkinter as ctk
from tkinter import messagebox
import os 
from dotenv import load_dotenv
import base64 
import hashlib
from cryptography.fernet import Fernet



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

load_dotenv()
KEY = os.getenv('SECURE_KEY')

class EditorTexto(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("Editor de texto")
		self.geometry("800x400")

		#TextArea
		self.textbox = ctk.CTkTextbox(self,width=580,
				height=300,
				fg_color="#1e1e1e",
				text_color="#dcdcdc",
				border_color="#3a3a3a",
				border_width=2)
		self.textbox.pack(pady=20,padx=10)

		self.save_button = ctk.CTkButton(self,text="Salvar em arquivo",command=self.salvar_texto)
		self.save_button.pack(pady=10)
	
	
		self.dcrypt_button = ctk.CTkButton(self,text="Descriptografar o arquivo",command=self.descriptografar)
		self.dcrypt_button.pack(pady=20)

	def gerar_chave(self,key_int:int)->bytes:
		#GERANDO UMA CHAVE DE 32 BYTES USANDO SHA256 + BASE64
		key_bytes = str(key_int).encode()
		hashed = hashlib.sha256(key_bytes).digest()
		return base64.urlsafe_b64encode(hashed)

	def criptografar(self,text:str,key_int:int)->str:
		fernet = Fernet(self.gerar_chave(key_int))
		return fernet.encrypt(text.encode()).decode()


	def salvar_texto(self):
		conteudoC = self.textbox.get("1.0","end").strip()
		conteudo =self.criptografar(conteudoC,KEY)
		try:
			with open("saida.txt","w",encoding="utf-8") as f:
				f.write(conteudo)
			messagebox.showinfo("Sucesso","Texto salvo em 'saida.txt'")

		except Exception as e:
			messagebox.showerror("Erro",str(e))

	def descriptografar(self):

		try:
			with open("saida.txt","r",encoding="utf-8") as f:
				conteudoC = f.read().strip()
			
			chave = str(KEY)
			fernet = Fernet(self.gerar_chave(chave))
			conteudoD = fernet.decrypt(conteudoC.encode().decode())
			self.textbox.delete("1.0","end")
			self.textbox.insert("1.0",conteudoD)
			messagebox.showinfo("Sucesso","Texto Descriptografado")
			print(conteudoD)
		except Exception as e:
			messagebox.showerror("Erro",str(e))


if __name__ =="__main__":
	app = EditorTexto()
	app.mainloop()
