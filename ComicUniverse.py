from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image

comics = []
personajes = []
usuarios = []

contCreacion = [1,1,1] #contadores de creacion = [cont Pagina, cont Escena, cont Dialogo]

comicCreacion = {'Titulo': '' ,'imagen':'','publicacion':'','escritor':'','dibujante':'','portada':'','sinopsis':'', 'paginas':[]}
paginaCreacion = {'Pagina': 0, 'imagen': '','escenas' :[]}
escenaCreacion = {'numero': 0,'imagen': '', 'dialogos':[]}
dialogoCreacion = {"numero": 0, "texto": '', "personaje": ''}

comicLeyendose = {}
modoLecturaActual = '' 
posActual = [-1,-1,-1] #posActual = [num Pagina, num Escena, num Dialogo]

comicEditandose = {}
modoEdicionActual = ''
posActualEditC = [0,0,0]

personajeEditandose = {}
posPersoEditandose = 0


#------------------- FILES FUNCIONES --------------------
#escribe en archivos I:direccion archivo O:
def escribir(nombreArchivo,strValue):
        fo = open(nombreArchivo, "w", encoding='utf-8')
        fo.write(strValue)
        fo.close()
#lee un archivo y guarda lo que tiene I:direccion archivo O:
def leer(nombreArchivo):
        fo = open(nombreArchivo, "r", encoding='utf-8')
        resultado = fo.read()
        fo.close()
        return resultado
#Sube el comic al archivo de comics I:O:
def subirComics():
        global comics
        comics = eval(leer("comics.py"))
#Sube el personajes al archivo de personajes I:O:
def subirPersonajes():
        global personajes
        personajes = eval(leer("personajes.py"))
#toma los usuarios del archivo de usuarios I:O:  
def subirUsuarios():
        global usuarios
        usuarios = eval(leer("usuarios.txt"))
#sube los users al archivo I:O:
def actualizarUsuarios():
        global usuarios
        escribir ("usuarios.txt", str(usuarios))
#sube los comics al archivo I:O:
def actualizarComics():
      global comics
      escribir ("comics.py", str(comics))
#sube los personajes al archivo I:O:
def actualizarPersonajes():
        global personajes
        escribir ("personajes.py", str(personajes))

fo = open("pinga.txt","w")
fo.write("pinga")
fo.close()

subirComics()
subirPersonajes()
subirUsuarios()

#---------LOGIN FUNCIONES---------
#comprueba la entrada del user y password I:keybind O:
def login(event=NONE):
    global usuarios
    inputUser = inputUsername.get()
    inputPass = inputPassword.get()
    flag = True
    
    for elem in usuarios:
        
         if elem[0] == inputUser and elem[1] == inputPass:
            tipoUsuario(elem[2])
            flag = False
    if flag:
        messagebox.showerror("Error de inicio de sesión.", "No coinciden usuario y contraseña.")

#habilita pestañas según tipo de usuario I: tipo usuario O:
def tipoUsuario(tipo):
        
        winLogin.withdraw()
        mainMenu.deiconify()
        print(tipo)
        tabControl.hide(0)
        tabControl.hide(1)
        tabControl.hide(2)
        tabControl.hide(3)
        
        if tipo.upper() == 'LECTOR':
                tabControl.add(leerTab, text='Leer')
                
        elif tipo.upper() == 'ESCRITOR':
                tabControl.add(crearTab, text='Crear')
                tabControl.add(editarTab, text='Editar')
        elif tipo.upper() == 'ADMIN':
                tabControl.add(usuariosTab, text='Usuarios')
        elif tipo.upper() == 'VERSATIL':
                tabControl.add(leerTab, text='Leer')
                tabControl.add(crearTab, text='Crear')
                tabControl.add(editarTab, text='Editar')

#---------LEER FUNCIONES------------
#funcion inicial para empezar a leer I: keybind O:
def leerComic(event):
       global comics, comicLeyendose, modoLecturaActual,lblImagenLeyendo
       if lbSugerencias.curselection():
                comicSeleccionado = lbSugerencias.get(lbSugerencias.curselection())
                for comic in comics:
                        if comic['Titulo'] == comicSeleccionado:
                                comicLeyendose = comic
                                modoLecturaActual = modoLectura.get()
                                mainMenu.withdraw()
                                winLeer.deiconify()

                                setImagen(comicLeyendose['imagen'])
                                setInfoPortada()

#busca un comic para leerlo I:keybind O:lista de sugerencias                                                   
def buscarComic(event=NONE):
        buscado = inputComicBuscado.get().lower()
        sugerencias = []
        if buscado != '':
                for comic in comics:
                        for pagina in comic['paginas']:
                                for escena in pagina['escenas']:
                                        for dialogo in escena['dialogos']:
                                                if (buscado.lower() in comic['Titulo'].lower() or buscado.lower() in dialogo['personaje'].lower()) and comic['Titulo'] not in sugerencias:
                                                        sugerencias+=[comic['Titulo']]
        lbSugerencias.delete(0, END)
        for sugerencia in sugerencias:
                lbSugerencias.insert(END, sugerencia)

#Hace un movimiento según tipo de lectura I: tipo lectura O:
def tipoLectura(mov):
        if modoLecturaActual == 'PxP':
                if mov == "siguiente":
                        siguientePag()
                else:
                        anteriorPag()
        elif modoLecturaActual == 'ExE':
                if mov == "siguiente":
                        siguienteEsc()
                else:
                        anteriorEsc()
        else:
                if mov == "siguiente":
                        siguienteDia()
                else:
                        anteriorDia()

#se fija si la direccion de la imagen es correcta I:direccion O:
def buscaImagen(img):
        try:
                Image.open(img)
                return True
        except:
                return False
        
#establece la imagen I:direccion O:
def setImagen(direccion):
        global lblImagenLeyendo

        if buscaImagen(direccion):
                nuevaImagen = Image.open(direccion)
                
        else:
                messagebox.showwarning('Direccion incorrecta', 'No se encontró la dirección de la imagen ingresada.')
                nuevaImagen = Image.open('no-img.png')

        nuevaImagen = nuevaImagen.resize((300, 425))
        nuevaImagen = ImageTk.PhotoImage(nuevaImagen)

        lblImagenLeyendo.configure(image=nuevaImagen)
        lblImagenLeyendo.image = nuevaImagen  

#pone la infor general del comic y la img de la portada I:O:
def setInfoPortada():
        global comicLeyendose, txtAreaDatos
        txtAreaDatos.config(state='normal')
        txtAreaDatos.delete('1.0', 'end')
        
        infoText = f"Comic: {comicLeyendose['Titulo']}\n\n"
        infoText += f"Publicación: {comicLeyendose['publicacion']}\n\n"
        infoText += f"Escritor: {comicLeyendose['escritor']}\n\n"
        infoText += f"Dibujante: {comicLeyendose['dibujante']}\n\n"
        infoText += f"Artista Portada: {comicLeyendose['portada']}\n\n"
        infoText += f"Sinopsis: {comicLeyendose['sinopsis']}\n\n"

        txtAreaDatos.insert('end', infoText + '\n')    
        txtAreaDatos.config(state='disabled')

#--------LEYENDO FUNCIONES---------     
#obtiene una pagina I: nom comic, num de pag O: pagina
def getPagina(titulo,numPag):
        global comics
        newList = ['',[]]
        for comic in comics:
                if comic['Titulo'] == titulo:
                        for escena in comic['paginas'][numPag]['escenas']:
                                newList[0] = comic['paginas'][numPag]['imagen']
                                for dialogo in escena['dialogos']:
                                        newList[1].append([dialogo['texto'],dialogo['personaje']])
        return newList

#mov de página hacia el frente
def siguientePag():
        global posActual, frameImagen, comicLeyendose, lblImagenLeyendo
         
        if posActual[0] == len(comicLeyendose['paginas']) - 1:
                messagebox.showinfo("Comic Finalizdo.", "No hay más contenido para leer.")
                return 
        posActual[0]+=1   
        nuevaPag = getPagina(comicLeyendose['Titulo'],posActual[0])

        dialogos = nuevaPag[1]
        setImagen(nuevaPag[0])
         

        txtAreaDatos.config(state='normal')
        txtAreaDatos.delete('1.0', 'end')
        infoText = ''
        for dialogo in dialogos:
            infoText += f"Dialogo: {dialogo[0]}\n"
            infoText += f"Personaje: {dialogo[1]}\n\n"
        txtAreaDatos.insert('end', infoText + '\n')
        txtAreaDatos.config(state='disabled')

#mov de página hacia atrás I:O:          
def anteriorPag():
        global posActual, frameImagen, comicLeyendose, lblImagenLeyendo
        
        if posActual[0] == -1:
                messagebox.showinfo("No hay páginas anteriores.", "Está en la portada xd.")
                return
        posActual[0]-=1
        
        if posActual[0] == -1:
                setImagen(comicLeyendose['imagen'])
                setInfoPortada()
                return 

        nuevaPag = getPagina(comicLeyendose['Titulo'],posActual[0])
        dialogos = nuevaPag[1]
        setImagen(nuevaPag[0])
        txtAreaDatos.config(state='normal')
        txtAreaDatos.delete('1.0', 'end')
        infoText = ''
        for dialogo in dialogos:
            infoText += f"Dialogo: {dialogo[0]}\n"
            infoText += f"Personaje: {dialogo[1]}\n\n"
        txtAreaDatos.insert('end', infoText + '\n')    
        txtAreaDatos.config(state='disabled')

#obtine escena I: nom comic, num de esc O: escena
def getEscena(titulo,numPag,numEsc):
        global comics
        print(titulo,numPag,numEsc)
        newList = ['',[]]
        for comic in comics:
                if comic['Titulo'] == titulo:
                        newList[0] = comic['paginas'][numPag]['escenas'][numEsc]['imagen']
                        for dialogo in comic['paginas'][numPag]['escenas'][numEsc]['dialogos']:
                                
                                newList[1].append([dialogo['texto'],dialogo['personaje']])
        return newList

#mov de escena hacia el frente
def siguienteEsc():
        global posActual, frameImagen, comicLeyendose, lblImagenLeyendo
        aux = posActual.copy()
        infoText = ''

        txtAreaDatos.config(state='normal')
        txtAreaDatos.delete('1.0', 'end')
        
        if posActual[0] == -1:
               posActual[1]=-1
               posActual[0] +=1
        if posActual[1] == len(comicLeyendose['paginas'][posActual[0]]['escenas'])-1 :
               posActual[0]+=1
               posActual[1]=-1
       
        if posActual[0] == len(comicLeyendose['paginas']):
                posActual = aux
                messagebox.showinfo("Comic Finalizdo.", "No hay más contenido para leer.")
                return 
        
        posActual[1]+=1
        print(posActual[0],posActual[1])
        nuevaEscena = getEscena(comicLeyendose['Titulo'],posActual[0],posActual[1])
        dialogos = nuevaEscena[1]

        setImagen(nuevaEscena[0])

        for dialogo in dialogos:
            infoText += f"Dialogo: {dialogo[0]}\n"
            infoText += f"Personaje: {dialogo[1]}\n\n"
        txtAreaDatos.insert('end', infoText + '\n')    
        txtAreaDatos.config(state='disabled')

#mov de escena hacia atrás I:O:   
def anteriorEsc():
        global posActual, frameImagen, comicLeyendose, lblImagenLeyendo
        
        if posActual[0] == -1:
                messagebox.showinfo("No hay páginas anteriores.", "Está en la portada xd.")
                return
        if posActual[1]-1 < 0:
               posActual[0] -= 1
               posActual[1] = len(comicLeyendose['paginas'][posActual[0]]['escenas'])
        if posActual[0] == -1:
                setImagen(comicLeyendose['imagen'])
                setInfoPortada()
                return 
        
        posActual[1] -= 1

        nuevaEscena = getEscena(comicLeyendose['Titulo'],posActual[0],posActual[1])
        dialogos = nuevaEscena[1]

        setImagen(nuevaEscena[0])

        txtAreaDatos.config(state='normal')
        txtAreaDatos.delete('1.0', 'end')
        infoText = ''
        for dialogo in dialogos:
            infoText += f"Dialogo: {dialogo[0]}\n"
            infoText += f"Personaje: {dialogo[1]}\n\n"
        txtAreaDatos.insert('end', infoText + '\n')    
        txtAreaDatos.config(state='disabled')

#obtine dialogo I: nom comic, num de dia O: dialogo
def getDialogo(titulo,numPag,numEsc,numDia):
        global comics
        newList = ['',[]]
        for comic in comics:
                if comic['Titulo'] == titulo:
                        newList[0] = comic['paginas'][numPag]['escenas'][numEsc]['imagen']
                        newList[1].append([comic['paginas'][numPag]['escenas'][numEsc]['dialogos'][numDia]['texto'],comic['paginas'][numPag]['escenas'][numEsc]['dialogos'][numDia]['personaje']])
        return newList

#mov de dialogo hacia el frente
def siguienteDia():
        global posActual, frameImagen, comicLeyendose, lblImagenLeyendo
        aux = posActual.copy()
        if posActual[0] == -1:
               posActual[2]=-1
               posActual[1] = 0
               posActual[0] = 0
        if posActual[2] == len(comicLeyendose['paginas'][posActual[0]]['escenas'][posActual[1]]['dialogos'])-1 :
               posActual[1]+=1
               posActual[2]=-1
        if posActual[1] == len(comicLeyendose['paginas'][posActual[0]]['escenas']) :
               posActual[0]+=1
               posActual[1]=0
               posActual[2]=-1
        if posActual[0] == len(comicLeyendose['paginas']):
                messagebox.showinfo("Comic Finalizdo.", "No hay más contenido para leer.")
                posActual = aux
                return 
        

        posActual[2]+=1
        print(posActual[0],posActual[1],posActual[2])
        nuevaEscena = getDialogo(comicLeyendose['Titulo'],posActual[0],posActual[1],posActual[2])
        dialogos = nuevaEscena[1]

        setImagen(nuevaEscena[0])

        txtAreaDatos.config(state='normal')
        txtAreaDatos.delete('1.0', 'end')
        infoText = ''
        for dialogo in dialogos:
            infoText += f"Dialogo: {dialogo[0]}\n"
            infoText += f"Personaje: {dialogo[1]}\n\n"
        txtAreaDatos.insert('end', infoText + '\n')    
        txtAreaDatos.config(state='disabled')

#mov de dialogo hacia atrás I:O:   
def anteriorDia():
        global posActual, frameImagen, comicLeyendose, lblImagenLeyendo
        aux = posActual
        if posActual[0] == -1:
                messagebox.showinfo("No hay páginas anteriores.", "Está en la portada xd.")
                return
        if posActual[2]-1 < 0:
               posActual[1] -=1
               posActual[2] = len(comicLeyendose['paginas'][posActual[0]]['escenas'][posActual[1]]['dialogos'])
        if posActual[1] < 0:
               posActual[0] -= 1
               posActual[1] = len(comicLeyendose['paginas'][posActual[0]]['escenas']) -1
               posActual[2] = len(comicLeyendose['paginas'][posActual[0]]['escenas'][posActual[1]]['dialogos'])
        if posActual[0] == -1:
                setImagen(comicLeyendose['imagen'])
                setInfoPortada()
                return 
        
        
        posActual[2] -= 1
        print(posActual[0],posActual[1],posActual[2])
        nuevoDialogo = getDialogo(comicLeyendose['Titulo'],posActual[0],posActual[1],posActual[2])
        dialogos = nuevoDialogo[1]

        setImagen(nuevoDialogo[0])

        txtAreaDatos.config(state='normal')
        txtAreaDatos.delete('1.0', 'end')
        infoText = ''
        for dialogo in dialogos:
            infoText += f"Dialogo: {dialogo[0]}\n"
            infoText += f"Personaje: {dialogo[1]}\n\n"
        txtAreaDatos.insert('end', infoText + '\n')    
        txtAreaDatos.config(state='disabled')

#region
#-------------CONSULTA PERSONAJE FUNCIONES--------------
#busca personaje para consultarlo I:keybind O:lista de sugerencias
def buscarPersonaje(event=NONE):
        global lbPersonajes
        buscado = inputPersonajeBuscado.get().lower()
        sugerencias = []
        if buscado != '':
                for pagina in comicLeyendose['paginas']:
                        for escena in pagina['escenas']:
                                for dialogo in escena['dialogos']:
                                        if buscado.lower() in dialogo['personaje'].lower() and dialogo['personaje'] not in sugerencias:
                                                sugerencias+=[dialogo['personaje']]
        lbPersonajes.delete(0, END)
        for sugerencia in sugerencias:
                lbPersonajes.insert(END, sugerencia)

#setea la info del personaje buscado anteriormente I:double click binding O:
def setInfoPersonaje(event=NONE):
        global personajes
        if lbPersonajes.curselection():
                nombrePerso = lbPersonajes.get(lbPersonajes.curselection())
                flag = True
                for perso in personajes:
                        if nombrePerso.lower() in perso['personaje'].lower() or nombrePerso.lower() in perso['nombre'].lower():
                                flag = False
                                txtAreaPersonaje.config(state='normal')
                                txtAreaPersonaje.delete('1.0', 'end')

                                infoText = f"Personaje: {perso['personaje']}\n\n"
                                infoText += f"Nombre: {perso['nombre']}\n\n"
                                infoText += f"Nacimiento: {perso['nacimiento']}\n\n"
                                infoText += f"Lugar de Origen: {perso['origen']}\n\n"
                                infoText += f"Lugar de residencia: {perso['reside']}\n\n"
                                infoText += f"Afiliaciones: {perso['afiliaciones']}\n\n"
                                infoText += f"Habilidades: {perso['habilidades']}\n\n"
                                infoText += f"Amor: {perso['amor']}\n\n"
                                infoText += f"Aliados: {perso['aliados']}\n\n"
                                infoText += f"Enemigos: {perso['enemigos']}\n\n"
                                infoText += f"Creador: {perso['reside']}\n\n"
                                infoText += f"Historia: {perso['historia']}\n\n"

                                txtAreaPersonaje.insert('end', infoText + '\n')    
                                txtAreaPersonaje.config(state='disabled')
                                return

                if flag:
                        messagebox.showinfo('No hay información', 'El personaje no contiene información adicional guardada.')

#------------USUARIOS FUNCIONES--------------------------
#obtiene posi de un usuario en la lista I:username y password O:pos
def getUserPos(userInput,passInput):
        global usuarios
        cont = 0
        for user in usuarios:
                if user[0] == userInput and user[1] == passInput:
                       return cont
                cont+=1
        return -1
#dice si un username está en uso I:username O:boolan
def userExistente(username):
        global usuarios
        for user in usuarios:
                if user[0] == username:
                       return True
        return False
#crea un usuario I:O:                
def crearUsuario():
        newUser = inputUsernameAdm.get()
        newPass = inputPasswordAdm.get()
        newTipo = tipoUserAdm.get()
        if not userExistente(newUser):
               usuarios.append([newUser,newPass,newTipo])
               messagebox.showinfo('Usuario creado','El usuario fue creado con éxito.')
               entryUserAdm.delete(0,'end')
               entryPassAdm.delete(0,'end')
               actualizarUsuarios()
        else:
                messagebox.showerror('Usuario no disponible','El nombre de usuario ya está en uso. Intenta con otro.')
#elimina un usuario I:O:
def eliminarUsuario():
        global usuarios
        newUser = inputUsernameAdm.get()
        newPass = inputPasswordAdm.get()
        posi = getUserPos(newUser,newPass)
        if posi != -1:
               del usuarios[posi]
               messagebox.showinfo('Usuario eliminado','El usuario fue eliminado con éxito.')
               entryUserAdm.delete(0,'end')
               entryPassAdm.delete(0,'end')
               actualizarUsuarios()

        else:
               messagebox.showerror('Usuario no existente','El usuario y la contraseña no coinciden. Intente de nuevo')
#modifica el tipo de un usuario I:O:
def modificarUsuario():
        global usuarios
        newUser = inputUsernameAdm.get()
        newPass = inputPasswordAdm.get()
        newTipo = tipoUserAdm.get()
        posi = getUserPos(newUser,newPass)
        if posi != -1:
                if usuarios[posi][2] == newTipo:
                      messagebox.showwarning('No se modificó el usuario.','Para modificar el usuario, ingrese un tipo distinto al que ya tiene.')
                else:
                        usuarios[posi][2] = newTipo
                        messagebox.showinfo("Usuario modificado",f"{newUser} ahora tiene permisos de {newTipo}.")
                        entryUserAdm.delete(0,'end')
                        entryPassAdm.delete(0,'end')
                        actualizarUsuarios()

        else:
               messagebox.showerror('Usuario no existente','El usuario y la contraseña no coinciden. Intente de nuevo')

#-------------------CREAR FUNCIONES---------------------
#empieza la creación de un cómic I: keybinding O:
def iniciarCreacion(event=NONE):
        global comicCreacion
        name = nomCrear.get()
        number = numeroCrear.get()
        writer = escritorCrear.get()
        penciler = dibujanteCrear.get()
        cover = portadaCrear.get()
        published = publicacionCrear.get()
        image = imagenCrear.get()
        description = txtAreaSinopsisCrear.get("1.0", "end-1c")

        if name == '' or number == '' or writer == '' or penciler == '' or cover == '' or published == '' or description == '':
                messagebox.showerror('Información incompleta','Complete toda la inforamción para poder iniciar con la creación del comic')
        if not image.strip():
                image = 'no-img.png'
        elif not isInt(number):
                messagebox.showerror('Edición con formato incorrecto','Para el número de edición solamente ingrese los dígitos.')
        elif not (image.lower().endswith('.jpg') or image.lower().endswith('.png')):
                messagebox.showerror('Formato de imagen incorrecto','Ingrese una imagen con extensión .png o .jpg para la portada. Verifique que la dirección sea la correcta para evitar errores.')
        else:
                name += ' #' + number
                comicCreacion['Titulo'] = name
                comicCreacion['dibujante'] = penciler
                comicCreacion['escritor'] = writer
                comicCreacion['portada'] = cover
                comicCreacion['publicacion'] = published
                comicCreacion['sinopsis'] = description
                comicCreacion['imagen'] = image
                comicCreacion['paginas'] = []
                winCrear.deiconify()
                mainMenu.withdraw()
                numDiaCreando.set(contCreacion[0])
                numEscCreando.set(contCreacion[1])
                numPagCreando.set(contCreacion[2])
#inserta un dialgo a la escena I:O:
def insertarDialogo():
        global contCreacion, dialogoCreacion, escenaCreacion
        dialogo = txtAreaTextoCreando.get('1.0',END)
        dialogo = dialogo[0:-1]
        personaje = personajeCreando.get()

        if not dialogo.strip() or not personaje.strip():
                messagebox.showerror('Información incompleta','Complete el diálogo con el personaje que lo dice para insertarlo.')
        else:   
                aux = dialogoCreacion.copy()
                aux['numero'] = contCreacion[2]
                aux['texto'] = dialogo
                aux['personaje'] = personaje
                
                escenaCreacion['dialogos'] += [aux] 
                contCreacion[2]+=1
                
                numDiaCreando.set(str(contCreacion[2]))
                txtAreaTextoCreando.delete("1.0", END)
                entryPersonajeCreando.delete(0, END)

                print(escenaCreacion)
#inserta una escena a la pag I:O:
def insertarEscena():
        global contCreacion, escenaCreacion, paginaCreacion
        imagen = entryImagenCreando.get()
        if not imagen.strip():
                imagen = 'no-img.png'
        if not (imagen.lower().endswith('.jpg') or imagen.lower().endswith('.png')):
                messagebox.showerror('Formato de imagen incorrecto','Ingrese una imagen con extensión .png o .jpg para la portada. Verifique que la dirección sea la correcta para evitar errores.')
        elif len(escenaCreacion['dialogos']) == 0:
                messagebox.showerror('No se puede insertar escena.','No tiene dialogos creados.')
        else:   
                aux = escenaCreacion.copy()
                aux['numero'] = contCreacion[1]
                aux['imagen'] = imagen
                
                paginaCreacion['escenas'] += [aux] 
                contCreacion[1]+=1
                contCreacion[2] = 1
                
                escenaCreacion['dialogos'] = []

                numDiaCreando.set(str(contCreacion[2]))
                numEscCreando.set(str(contCreacion[1]))
                entryImagenCreando.delete(0, END)

                print(paginaCreacion)
#inserta una pag al comic I:O:
def insertarPagina():
        global contCreacion,paginaCreacion, comicCreacion
        imagen = entryImagenPaginaCreando.get()
        if not imagen.strip():
                imagen = 'no-img.png'
        if not (imagen.lower().endswith('.jpg') or imagen.lower().endswith('.png')):
                messagebox.showerror('Formato de imagen de página incorrecto','Ingrese una imagen con extensión .png o .jpg para la portada. Verifique que la dirección sea la correcta para evitar errores.')
        elif len(paginaCreacion['escenas']) == 0:
                messagebox.showerror('No se puede insertar página.','No tiene escenas creadas.')
        else:   
                aux = paginaCreacion.copy()
                aux['Pagina'] = contCreacion[0]
                aux['imagen'] = imagen
                
                comicCreacion['paginas'] += [aux] 

                contCreacion[0]+=1
                contCreacion[1] = 1
                contCreacion[2] = 1

                paginaCreacion['escenas'] = []

                numDiaCreando.set(str(contCreacion[2]))
                numEscCreando.set(str(contCreacion[1]))
                numPagCreando.set(str(contCreacion[0]))

                entryImagenPaginaCreando.delete(0, END)

                print(comicCreacion)
#limpia los restos de la creacion del comic I:O:
def terminarComic():
        global contCreacion, comicCreacion
        contCreacion = [1,1,1] 
        comicCreacion = {'Titulo': '' ,'imagen':'','publicacion':'','escritor':'','dibujante':'','portada':'','sinopsis':'', 'paginas':[]}
        
        txtAreaTextoCreando.delete('1.0',END)
        entryImagenCreando.delete(0, END)
        entryImagenPaginaCreando.delete(0, END)
        entryPersonajeCreando.delete(0, END)

        entryNomCrear.delete(0, END)
        entryNumeroCrear.delete(0, END)
        entryEscritorCrear.delete(0, END)
        entryDibujanteCrear.delete(0, END)
        entryPortadaCrear.delete(0, END)
        entryPublicacionCrear.delete(0, END)
        entryImagenCrear.delete(0, END)
        txtAreaSinopsisCrear.delete('1.0', END)
        messagebox.showinfo('Comic creado', 'Se ha creado el cómic exitosamente')
        winCrear.withdraw()
        mainMenu.deiconify()
#inserta un comic a la lista de comics I:O:
def insertarComic():
        global comicCreacion,contCreacion, comics

        aux = comicCreacion.copy()
        comics += [aux]
        actualizarComics()
        terminarComic()
#dice si un dato es INT I:dato O:boolean  
def isInt(dato):
        try:
                int(dato)
                return True
        except:
                return False
#limpia los entrys y txt's de las ventanas I:O:
def limpiarVentanas():
        global posActual, comicLeyendose, txtAreaDatos, txtAreaPersonaje, comicEditandose, posActualEditC
        txtAreaDatos.config(state='normal')
        txtAreaPersonaje.config(state='normal')
        posActualEditC = [0,0,0]
        posActual = [-1,-1,-1]
        comicLeyendose = {}
        comicEditandose = {}
        lbSugerencias.delete(0,'end')
        entryComicBuscado.delete(0,'end')
        txtAreaDatos.delete('1.0', 'end')
        lbPersonajes.delete(0,'end')
        entryPersonajeBuscado.delete(0,'end')
        txtAreaPersonaje.delete('1.0', 'end')

        txtAreaDatos.config(state='disabled')
        txtAreaPersonaje.config(state='disabled')
        limpiarEditPersonajes()
#abre una ventana y cierra otra I:ventana por cerrar y por abrir O:
def salir(wCerrar,wAbrir):
        limpiarVentanas()
        if wAbrir != '':
                wAbrir.deiconify()
                wCerrar.withdraw()
        else:
               wCerrar.destroy()
#centra el popeo de una ventana con respecto al monitor I:tamaño de ventana y la ventana O:
def centerWindow(size,window):
        anchoPantalla2 = window.winfo_screenwidth()
        altoPantalla2 = window.winfo_screenheight()
        x3 = (anchoPantalla2 // 2) - (size // 2)
        y3 = (altoPantalla2 // 2) - (size // 2)
        size = str(size)
        window.geometry(f"{size}x{size}+{x3}+{y3}")

#------------------EDITAR PERSONAJE--------------------------
#busca personajes para editar I:keybinding O:lista de sugerencias
def buscarPersoEditar(event=NONE):
        global personajes
        buscado = persoBuscadoEdit.get()
        sugerencias = []
        if buscado != '':
                for perso in personajes:
                        if (buscado.lower() in perso['nombre'].lower() or buscado.lower() in perso['personaje'].lower()) and perso['personaje'] not in sugerencias:
                                sugerencias += [perso['personaje']]
        lbPersoBuscadoEdit.delete(0, END)
        for sugerencia in sugerencias:
                lbPersoBuscadoEdit.insert(END, sugerencia)
#obtiene la info de un personaje en la lista de personajes I:nombre del personaje O:
def getInfoPersonajeEditP(personaje):
        global personajeEditandose, personajes, posPersoEditandose
        posPersoEditandose = 0
        for perso in personajes:
                if perso['personaje'] == personaje:
                        personajeEditandose = perso
                        return
                posPersoEditandose +=1
#setea la info del personaje en los entries para editarla I:keybind O:
def seleccionarEditP(event=None):
        global personajes
        if lbPersoBuscadoEdit.curselection():
                personaje = lbPersoBuscadoEdit.get(lbPersoBuscadoEdit.curselection())
                getInfoPersonajeEditP(personaje)
                personajeEditP.set(personajeEditandose['personaje'])
                nombreEditP.set(personajeEditandose['nombre'])
                nacimientoEditP.set(personajeEditandose['nacimiento'])
                origenEditP.set(personajeEditandose['origen'])
                resideEditP.set(personajeEditandose['reside'])
                afiliacionesEditP.set(personajeEditandose['afiliaciones'])
                habilidadesEditP.set(personajeEditandose['habilidades'])
                amorEditP.set(personajeEditandose['amor'])
                creadorEditP.set(personajeEditandose['creador'])
                aliadosEditP.set(personajeEditandose['aliados'])
                enemigosEditP.set(personajeEditandose['enemigos'])
                txtAreaHistoriaEditP.delete('1.0', 'end')
                txtAreaHistoriaEditP.insert('end', personajeEditandose['historia'])
#limpia los entries de la edicion de personaje I: O:
def limpiarEditPersonajes():
        entryNombreEditP.delete(0,'end')
        entryPersonajeEditP.delete(0,'end')
        entryNacimientoEditP.delete(0,'end')
        entryOrigenEditP.delete(0,'end')
        entryResideEditP.delete(0,'end')
        entryAfiliacionesEditP.delete(0,'end')
        entryHabilidadesEditP.delete(0,'end')
        entryAmorEditP.delete(0,'end')
        entryCreadorEditP.delete(0,'end')
        entryAliadosEditP.delete(0,'end')
        entryEnemigosEditP.delete(0,'end')
        txtAreaHistoriaEditP.delete('1.0', 'end')
        entryPersoBuscadoEdit.delete(0,'end')
        lbPersoBuscadoEdit.delete(0,END)
#cambia la info del personaje por la nueva I:O:
def modificarPersonaje():
        global comicEditandose, personajes, personajeEditandose, posPersoEditandose
        personajeEditandose['personaje'] = personajeEditP.get()
        personajeEditandose['nombre'] = nombreEditP.get()
        personajeEditandose['nacimiento'] = nacimientoEditP.get()
        personajeEditandose['origen'] = origenEditP.get()
        personajeEditandose['reside'] = resideEditP.get()
        personajeEditandose['afiliaciones'] = afiliacionesEditP.get()
        personajeEditandose['amor'] = amorEditP.get()
        personajeEditandose['creador'] = creadorEditP.get()
        personajeEditandose['aliados'] = aliadosEditP.get()
        personajeEditandose['enemigos'] = enemigosEditP.get()
        personajeEditandose['historia'] = txtAreaHistoriaEditP.get('1.0',END)

        personajes[posPersoEditandose] = personajeEditandose
        messagebox.showinfo('Información actualizada.','Se ha modificado la información de '+personajeEditandose['personaje'])
        limpiarEditPersonajes()
        actualizarPersonajes()
        personajeEditandose = []
        posPersoEditandose = 0
#obtiene los personajes que están en uso en los comics I:O:lista
def getPersosEnComics():
        global comics
        res = []
        for comic in comics:
                for pagina in comic['paginas']:
                        for escena in pagina['escenas']:
                                for dialogo in escena['dialogos']:
                                        if [dialogo['personaje'],comic['Titulo']] not in res:
                                                res+=[[dialogo['personaje'], comic['Titulo']]]
        return res
#elimina un personaje I: O:
def eliminarPersonaje():
        global personajes, posPersoEditandose, personajeEditandose
        enComics = getPersosEnComics()
        apariciones = ''
        for persoComic in enComics:
                if persoComic[0].lower() in personajes[posPersoEditandose]['personaje'].lower() or persoComic[0].lower() in personajes[posPersoEditandose]['nombre'].lower():
                        apariciones += persoComic[1]+'  '
        if apariciones != '':
                messagebox.showerror('No se puede eliminar','El personaje aparece en los siguientes cómics: '+apariciones)
        else:
                del personajes[posPersoEditandose]
                actualizarPersonajes()
                messagebox.showinfo('Personaje eliminado.','Se ha eliminado la información de '+personajeEditandose['personaje'])
                limpiarEditPersonajes()
                personajeEditandose = []
                posPersoEditandose = 0
#endregion
#-------------------EDITAR COMIC--------------------------------
#busca comics para editar I:keybinding O:lista de sugerencias
def buscarComicEditarC(event=NONE):
        buscado = inputComicBuscadoEditC.get().lower()
        sugerencias = []
        if buscado != '':
                for comic in comics:
                        for pagina in comic['paginas']:
                                for escena in pagina['escenas']:
                                        for dialogo in escena['dialogos']:
                                                if (buscado.lower() in comic['Titulo'].lower() or buscado.lower() in dialogo['personaje'].lower()) and comic['Titulo'] not in sugerencias:
                                                        sugerencias+=[comic['Titulo']]
        lbSugerenciasEditC.delete(0, END)
        for sugerencia in sugerencias:
                lbSugerenciasEditC.insert(END, sugerencia)
#modifica la ventana de edición I:tipo de edicion O:lista de sugerencias
def cambiarVentanaEditC(tipo):
        entryPersoSelecEditC.place_forget()
        personajeLableEditC.set('')
        if tipo == 'Pag':
                lblEscEditando.place_forget()
                numEscEditando.set('')
                lblDiaEditando.place_forget()
                numDiaEditando.set('')
                txtAreaDiaSelecEditC.config(state='disabled')

        elif tipo == 'Esc':
                lblDiaEditando.place_forget()
                lblEscEditando.place(x = 260, y = 130)
                numDiaEditando.set('')
                txtAreaDiaSelecEditC.config(state='disabled')
        else:
                lblEscEditando.place(x = 260, y = 130)
                lblDiaEditando.place(x = 320, y = 130)
                entryPersoSelecEditC.place(x = 10, y = 300)
                personajeLableEditC.set('Personaje')
                txtAreaDiaSelecEditC.config(state='normal')
#función inicial para comenzar a editar el comic I:flag lógico inicializado O:
def editarComic(flag=False):
        global comicEditandose, modoEdicionActual, posActualEditC
        if lbSugerenciasEditC.curselection() or flag:
                if not flag:
                        comicSeleccionado = lbSugerenciasEditC.get(lbSugerenciasEditC.curselection())
                else:
                        comicSeleccionado = comicEditandose['Titulo']
                print('DATO:',comicSeleccionado)
                for comic in comics:
                        if comic['Titulo'] == comicSeleccionado:
                                comicEditandose = comic
                                modoEdicionActual = modoEdicion.get()
                                mainMenu.withdraw()
                                winEditarComic.deiconify()
                                posActualEditC =[0,0,0]
                                if modoEdicionActual == 'Dialogos':
                                        posActualEditC[2]-=1
                                        setDiaSig()
                                        cambiarVentanaEditC('Dia')
                                elif modoEdicionActual == 'Escenas':
                                        posActualEditC[1]-=1
                                        setEscSig()
                                        cambiarVentanaEditC('Esc')

                                else:
                                        posActualEditC[0]-=1
                                        setPagSig()
                                        cambiarVentanaEditC('Pag')
#se fija el tipo de edición que se está usando y hace el mov I:tipo de edición O:
def tipoEdicion(tipo):
        if tipo == 'Siguiente':
                if modoEdicionActual == 'Dialogos':
                        setDiaSig()
                elif modoEdicionActual == 'Escenas':
                        setEscSig()
                else:
                        setPagSig()
        else:
                if modoEdicionActual == 'Dialogos':
                        setDiaAnt()
                elif modoEdicionActual == 'Escenas':
                        setEscAnt()
                else:
                        setPagAnt()
#dice el max posible de intercambio de posiiciones I:O:
def getMaxPosible():
        if modoEdicionActual == 'Dialogos':
                return len(comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]]['dialogos']) 
        elif modoEdicionActual == 'Escenas':
                return len(comicEditandose['paginas'][posActualEditC[0]]['escenas'])
        else:
                return len(comicEditandose['paginas']) 
#setea la info del siguiente dialogo I:O:
def setDiaSig():
        global posActualEditC, comicEditandose
        aux = posActualEditC.copy()
        print('Before:',posActualEditC[0],posActualEditC[1],posActualEditC[2])
        posActualEditC[2]+=1
        if posActualEditC[2] == len(comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]]['dialogos']):
               posActualEditC[1]+=1
               posActualEditC[2]=0
        if posActualEditC[1] == len(comicEditandose['paginas'][posActualEditC[0]]['escenas']) :
               posActualEditC[0]+=1
               posActualEditC[1]=0
               posActualEditC[2]=0
        if posActualEditC[0] == len(comicEditandose['paginas']):
                messagebox.showinfo("Comic Finalizdo.", "No hay más contenido para leer.")
                posActualEditC = aux
                return 
                                    
        nuevaPag = getDialogo(comicEditandose['Titulo'],posActualEditC[0],posActualEditC[1],posActualEditC[2])
        
        dialogos = nuevaPag[1]
        txtAreaDiaSelecEditC.delete('1.0', 'end')
        txtAreaDiaSelecEditC.insert('end', dialogos[0][0])

        persoSelecEditC.set(dialogos[0][1])
        posMaximaNum.set(getMaxPosible())
        
        print('After:',posActualEditC[0],posActualEditC[1],posActualEditC[2])
        numDiaEditando.set(posActualEditC[2]+1)
        numEscEditando.set(posActualEditC[1]+1)
        numPagEditando.set(posActualEditC[0]+1)
        
        posSelecEditC.set(posActualEditC[2]+1)
#setea la info del anterior dialogo I:O:
def setDiaAnt():
        global posActualEditC, comicEditandose
        aux = posActualEditC.copy()
        print('Before:',posActualEditC[0],posActualEditC[1],posActualEditC[2])
        if posActualEditC[2] <= 0:
               posActualEditC[1] -=1
               posActualEditC[2] = len(comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]]['dialogos'])
        if posActualEditC[1] < 0:
               posActualEditC[0] -= 1
               posActualEditC[1] = len(comicEditandose['paginas'][posActualEditC[0]]['escenas']) -1
               posActualEditC[2] = len(comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]]['dialogos'])
        if posActualEditC[0] < 0:
                messagebox.showinfo('No puede retroceder más','Está en el inicio del cómic')
                posActualEditC = aux
                return
        
        
        posActualEditC[2] -= 1
        print('After:',posActualEditC[0],posActualEditC[1],posActualEditC[2])
        nuevoDialogo = getDialogo(comicEditandose['Titulo'],posActualEditC[0],posActualEditC[1],posActualEditC[2])
        dialogos = nuevoDialogo[1]

        txtAreaDiaSelecEditC.delete('1.0', 'end')
        txtAreaDiaSelecEditC.insert('end', dialogos[0][0])

        persoSelecEditC.set(dialogos[0][1])
        posMaximaNum.set(getMaxPosible())
        
        numDiaEditando.set(posActualEditC[2]+1)
        numEscEditando.set(posActualEditC[1]+1)
        numPagEditando.set(posActualEditC[0]+1)
        posSelecEditC.set(posActualEditC[2]+1)
#setea la info de la siguiente escena I:O:
def setEscSig():
        global posActualEditC, frameImagen, comicEditandose
        aux = posActualEditC.copy()
        
        print('Before:',posActualEditC[0],posActualEditC[1])
        posActualEditC[1]+=1
        if posActualEditC[1] == len(comicEditandose['paginas'][posActualEditC[0]]['escenas']):
               posActualEditC[0]+=1
               posActualEditC[1]=0
        if posActualEditC[0] == len(comicEditandose['paginas']):
                messagebox.showinfo("Comic Finalizdo.", "No hay más contenido para leer.")
                posActualEditC = aux
                return 
        
        nuevaEscena = getEscena(comicEditandose['Titulo'],posActualEditC[0],posActualEditC[1])
        dialogos = nuevaEscena[1]
        
        print('After:',posActualEditC[0],posActualEditC[1])
        infoText = ''
        for dialogo in dialogos:
            infoText += f"Dialogo: {dialogo[0]}\n"
            infoText += f"Personaje: {dialogo[1]}\n\n"
        txtAreaDiaSelecEditC.config(state='normal')
        txtAreaDiaSelecEditC.delete('1.0', 'end')
        txtAreaDiaSelecEditC.insert('end', infoText + '\n')
        txtAreaDiaSelecEditC.config(state='disabled')   

        
        posMaximaNum.set(getMaxPosible())
        numEscEditando.set(posActualEditC[1]+1)
        numPagEditando.set(posActualEditC[0]+1)
        posSelecEditC.set(posActualEditC[1]+1)
#setea la info de la anterior escena I:O:
def setEscAnt():
        global posActualEditC, comicEditandose
        aux = posActualEditC.copy()

        if posActualEditC[1] <= 0:
               posActualEditC[0] -= 1
               posActualEditC[1] = len(comicEditandose['paginas'][posActualEditC[0]]['escenas']) 
        if posActualEditC[0] < 0:
                messagebox.showinfo('No puede retroceder más','Está en el inicio del cómic')
                posActualEditC = aux
                return
        
        posActualEditC[1] -= 1

        nuevaEscena = getEscena(comicEditandose['Titulo'],posActualEditC[0],posActualEditC[1])
        dialogos = nuevaEscena[1]
        
        infoText = ''
        for dialogo in dialogos:
            infoText += f"Dialogo: {dialogo[0]}\n"
            infoText += f"Personaje: {dialogo[1]}\n\n"
        txtAreaDiaSelecEditC.config(state='normal')
        txtAreaDiaSelecEditC.delete('1.0', 'end')
        txtAreaDiaSelecEditC.insert('end', infoText + '\n')
        txtAreaDiaSelecEditC.config(state='disabled')   

        
        posMaximaNum.set(getMaxPosible())
        numEscEditando.set(posActualEditC[1]+1)
        numPagEditando.set(posActualEditC[0]+1)
        posSelecEditC.set(posActualEditC[1]+1)
#setea la info de la siguiente pagina I:O:
def setPagSig():
        global posActualEditC, frameImagen, comicEditandose
        aux = posActualEditC.copy()
        
        posActualEditC[0]+=1
        if posActualEditC[0] == len(comicEditandose['paginas']):
                messagebox.showinfo("Comic Finalizdo.", "No hay más contenido para leer.")
                posActualEditC = aux
                return 
        
        nuevaPag = getPagina(comicEditandose['Titulo'],posActualEditC[0])
        dialogos = nuevaPag[1]
        
        infoText = ''
        for dialogo in dialogos:
            infoText += f"Dialogo: {dialogo[0]}\n"
            infoText += f"Personaje: {dialogo[1]}\n\n"
        txtAreaDiaSelecEditC.config(state='normal')
        txtAreaDiaSelecEditC.delete('1.0', 'end')
        txtAreaDiaSelecEditC.insert('end', infoText + '\n')
        txtAreaDiaSelecEditC.config(state='disabled')   

        
        posMaximaNum.set(getMaxPosible())
        numPagEditando.set(posActualEditC[0]+1)
        posSelecEditC.set(posActualEditC[0]+1)
#setea la info de la anterior pagina I:O:
def setPagAnt():
        global posActualEditC, comicEditandose
        aux = posActualEditC.copy()
        if posActualEditC[0] <= 0:
                messagebox.showinfo('No puede retroceder más','Está en el inicio del cómic')
                posActualEditC = aux
                return
        
        posActualEditC[0] -= 1

        nuevaPag = getPagina(comicEditandose['Titulo'],posActualEditC[0])
        dialogos = nuevaPag[1]
        
        infoText = ''
        for dialogo in dialogos:
            infoText += f"Dialogo: {dialogo[0]}\n"
            infoText += f"Personaje: {dialogo[1]}\n\n"
        txtAreaDiaSelecEditC.config(state='normal')
        txtAreaDiaSelecEditC.delete('1.0', 'end')
        txtAreaDiaSelecEditC.insert('end', infoText + '\n')
        txtAreaDiaSelecEditC.config(state='disabled')   

        
        posMaximaNum.set(getMaxPosible())
        numPagEditando.set(posActualEditC[0]+1)
        posSelecEditC.set(posActualEditC[0]+1)
#actualiza el comic I:O:
def atualizaComicEditC():
        global comicEditandose, posActualEditC
        newPosi = posSelecEditC.get() 
        newPerso = persoSelecEditC.get()
        newText = txtAreaDiaSelecEditC.get('1.0',END)
        newText = newText[0:-1]
        print('Modo Edición:',modoEdicionActual)
        if not isInt(newPosi):
                messagebox.showerror('Posición inváida','Ingrese un numerito entre el rango.')
                return 
        newPosi = int(newPosi) - 1
        
        if modoEdicionActual == 'Dialogos':
                if 0 <= newPosi < len(comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]]['dialogos']):
                        comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]]['dialogos'][posActualEditC[2]], comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]]['dialogos'][newPosi] =  comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]]['dialogos'][posActualEditC[2]], comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]]['dialogos'][posActualEditC[2]]

                        comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]]['dialogos'][newPosi]['personaje'] = newPerso
                        comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]]['dialogos'][newPosi]['texto'] = newText

                else:
                        messagebox.showerror('No puede hacerse el intercambio de Posiciones','No se puede colocar el dialogo en dicha posición. Fíjese en los rangos posibles.')
                        return
        elif modoEdicionActual == 'Escenas':
                if 0 <= newPosi < len(comicEditandose['paginas'][posActualEditC[0]]['escenas']):
                        comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]], comicEditandose['paginas'][posActualEditC[0]]['escenas'][newPosi] =  comicEditandose['paginas'][posActualEditC[0]]['escenas'][newPosi], comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]]
                else:
                        messagebox.showerror('No puede hacerse el intercambio de Posiciones','No se puede colocar la escena en dicha posición. Fíjese en los rangos posibles.')
                        return
        else:
                if 0 <= newPosi < len(comicEditandose['paginas']):
                        comicEditandose['paginas'][posActualEditC[0]], comicEditandose['paginas'][newPosi] =  comicEditandose['paginas'][newPosi], comicEditandose['paginas'][posActualEditC[0]]
                else:
                        messagebox.showerror('No puede hacerse el intercambio de Posiciones','No se puede colocar la página en dicha posición. Fíjese en los rangos posibles.')
                        return
        
        for comic in comics:
                if comic['Titulo'] == comicEditandose['Titulo']:
                        comic = comicEditandose
        messagebox.showinfo('Comic Actualizado','La información del cómic se actualizó exitosamente')
        actualizaIndices()
        actualizarComics()
        editarComic(True)
#elimina parte del comic según tipo de edicion I:O:    
def eliminarParte():
        global comics, comicEditandose
        if modoEdicionActual == 'Dialogos':
                del comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]]['dialogos'][posActualEditC[2]]
                messagebox.showinfo('Dialogo Eliminado','Dialogo eliminado exitosamente')
        elif modoEdicionActual == 'Escenas':
                del comicEditandose['paginas'][posActualEditC[0]]['escenas'][posActualEditC[1]]
                messagebox.showinfo('Escena Eliminada','Escena eliminada exitosamente')
        else:
                del comicEditandose['paginas'][posActualEditC[0]]
                messagebox.showinfo('Páginas Eliminada','Página eliminada exitosamente')
        for comic in comics:
                if comic['Titulo'] == comicEditandose['Titulo']:
                        comic = comicEditandose
        desfragmentar()
        actualizaIndices()
        actualizarComics()
        editarComic(True)
#elimina todo el comic I:O:
def eliminarComic():
        global comicEditandose, modoEdicionActual, comics
        if lbSugerenciasEditC.curselection():
                comicSeleccionado = lbSugerenciasEditC.get(lbSugerenciasEditC.curselection())
                for comic in comics:
                        if comic['Titulo'] == comicSeleccionado:
                                messagebox.showinfo('Cómic eliminado','Se ha eliminado '+comic['Titulo']+' de la lista de cómics.')
                                comics.remove(comic)
                                print(comics)
                                comicEditandose = []
                                entryComicBuscadoEditC.delete(0,END)
                                lbSugerenciasEditC.delete(0,END)
                                actualizarComics()
                                return
#desfragemnta espacion vacios en el comic I:O:                  
def desfragmentar():
        global comicEditandose
        for pagina in comicEditandose['paginas']:
                
                if len(pagina['escenas']) == 0:
                        comicEditandose['paginas'].remove(pagina)
                else:
                        for escena in pagina['escenas']:
                                if len(escena['dialogos']) == 0:
                                        pagina['escenas'].remove(escena)
                                        desfragmentar()
                                        return
#actualiza los indices del comic I:O:
def actualizaIndices():
        global comicEditandose
        contPag = 1
        for pag in comicEditandose['paginas']:
                contEsc = 1
                for esc in pag['escenas']:
                        contDia = 1
                        for dia in esc['dialogos']:
                                dia['numero'] = contDia
                                contDia += 1
                        contDia =1
                        esc['numero'] = contEsc
                        contEsc += 1
                contEsc = 1
                pag['Pagina'] = contPag
                contPag += 1



#-------------VENTANAS------------
#region Esta región es la creación de toda la Gui del programa
winLogin = Tk()
winLogin.title("Login")
centerWindow(300,winLogin)

mainMenu = Toplevel(winLogin)
mainMenu.title("Comic Universe")
centerWindow(300,mainMenu)
mainMenu.withdraw() 

winLeer = Toplevel(winLogin)
winLeer.title("Leer Comic")
centerWindow(700,winLeer)
winLeer.geometry("700x500")
winLeer.withdraw()
winLeer.tk.call('encoding', 'system', 'utf-8')

winCrear = Toplevel(winLogin)
winCrear.title("Crear Comic")
centerWindow(300,winCrear)
winCrear.withdraw() 
winCrear.tk.call('encoding', 'system', 'utf-8')

winEditarComic = Toplevel(winLogin)
winEditarComic.title("Editar Cómic")
centerWindow(400,winEditarComic)
winEditarComic.withdraw()
winEditarComic.tk.call('encoding', 'system', 'utf-8')

winEditarPerso = Toplevel(winLogin)
winEditarPerso.title("Editar Personaje")
centerWindow(500,winEditarPerso)
winEditarPerso.withdraw() 
winEditarPerso.tk.call('encoding', 'system', 'utf-8')


tabControl = ttk.Notebook(mainMenu)

leerTab = Frame(tabControl)
tabControl.add(leerTab, text='Leer')

crearTab = Frame(tabControl)
tabControl.add(crearTab, text='Crear')

editarTab = Frame(tabControl)
tabControl.add(editarTab, text='Editar')

usuariosTab = Frame(tabControl)
tabControl.add(usuariosTab, text='Usuarios')

tabControl.pack(expand=1,fill='both')

#----------------LOGIN WINDOW----------------

inputUsername = StringVar()
inputPassword = StringVar()

username_label = Label(winLogin, text="Username:").place(x = 120, y = 50)
username_entry = Entry(winLogin, textvariable=inputUsername)
username_entry.place(x = 90, y = 75)

password_label = Label(winLogin, text="Password:").place(x = 120, y = 120)
password_entry = Entry(winLogin, show="*", textvariable=inputPassword)
password_entry.place(x = 90, y = 145)
login_button = Button(winLogin, text="Iniciar sesión", command=login).place(x = 110, y = 180) 
btnSalirLogin = Button(winLogin, text="Salir", command=lambda: salir(winLogin,''), width="10").place(x = 110, y = 230) 

username_entry.bind("<Return>", login)
password_entry.bind("<Return>", login)

#----------------LEER TAB----------------

inputComicBuscado = StringVar()

modoLectura = StringVar(value='PxP')

lblComicBuscado = Label(leerTab, text="Buscar Comic").place(x = 40, y = 10)

entryComicBuscado = Entry(leerTab, textvariable=inputComicBuscado)
entryComicBuscado.place(x = 20, y = 40)

lbSugerencias = Listbox(leerTab)
lbSugerencias.place(x = 20, y = 70)

rbn1 = Radiobutton(leerTab, text='Leer por Página', variable=modoLectura, value='PxP')
rbn1.place(x=170, y=70)
rbn2 = Radiobutton(leerTab, text='Leer por Escena', variable=modoLectura, value='ExE')
rbn2.place(x=170, y=90)
rbn3 = Radiobutton(leerTab, text='Leer por Dialogo', variable=modoLectura, value='DxD')
rbn3.place(x=170, y=110)

btnSalirLeerTab = Button(leerTab, text="Salir", command=lambda: salir(mainMenu,winLogin), width="10").place(x = 180, y = 200) 

entryComicBuscado.bind("<Return>", buscarComic)
lbSugerencias.bind("<Double-Button-1>", leerComic)

#----------------LEYENDO TAB----------------

tabControlReading = ttk.Notebook(winLeer)

leyendoTab = Frame(tabControlReading)
tabControlReading.add(leyendoTab, text='Leyendo Comic')

consultarTab = Frame(tabControlReading)
tabControlReading.add(consultarTab, text='Consultar')

tabControlReading.pack(expand=1,fill='both')

frameImagen = Frame(leyendoTab, width=300, height=425)  
frameImagen.place(x=30,y=20)
 
lblImagenLeyendo = Label(frameImagen)
lblImagenLeyendo.pack()

btnAnterior = Button(leyendoTab, text="Anterior", command=lambda: tipoLectura('anterior'), width="12").place(x = 350, y = 410) 
btnSiguiente = Button(leyendoTab, text="Siguiente", command=lambda: tipoLectura('siguiente'), width="12").place(x = 460, y = 410) 
btnSalirLeyendoTab = Button(leyendoTab, text="Salir", command=lambda: salir(winLeer,mainMenu), width="12").place(x = 570, y = 410) 


txtAreaDatos = Text(leyendoTab, state='disabled', width=38, height=23)
scrollbarLeyendo = Scrollbar(leyendoTab, command=txtAreaDatos.yview)
scrollbarLeyendo.pack(side=RIGHT, fill=Y)
txtAreaDatos.place(x=350, y = 20)
txtAreaDatos.config(yscrollcommand=scrollbarLeyendo.set)

#----------------CONSULTA TAB----------------
inputPersonajeBuscado = StringVar()


lblConsultarPersonaje = Label(consultarTab, text="Consulta Personaje").place(x = 85, y = 20)
lblPersonajeBuscado = Label(consultarTab, text="Info del Personaje").place(x = 430 , y = 50)

entryPersonajeBuscado = Entry(consultarTab, textvariable=inputPersonajeBuscado)
entryPersonajeBuscado.place(x = 77, y = 50)


lbPersonajes = Listbox(consultarTab, width=40, height=22)
lbPersonajes.place(x = 30, y = 90)

txtAreaPersonaje = Text(consultarTab, state='disabled', width=45, height=22)
scrollbarConsultar = Scrollbar(consultarTab, command=txtAreaPersonaje.yview)
scrollbarConsultar.pack(side=RIGHT, fill=Y)
txtAreaPersonaje.place(x=300, y = 90)
txtAreaPersonaje.config(yscrollcommand=scrollbarConsultar.set)

entryPersonajeBuscado.bind("<Return>", buscarPersonaje)
lbPersonajes.bind("<Double-Button-1>", setInfoPersonaje)

#-------------------USUARIOS TAB------------------

inputUsernameAdm = StringVar()
inputPasswordAdm = StringVar()
tipoUserAdm = StringVar(value='lector')

lblUserAdm = Label(usuariosTab, text="Username").place(x = 50, y = 10)
entryUserAdm = Entry(usuariosTab, textvariable=inputUsernameAdm)
entryUserAdm.place(x = 15, y = 40)

lblPassAdm = Label(usuariosTab, text="Password").place(x = 190, y = 10)
entryPassAdm = Entry(usuariosTab, textvariable=inputPasswordAdm)
entryPassAdm.place(x = 155, y = 40)

btnDeleteUser = Button(usuariosTab, text="Eliminar", command=eliminarUsuario, width="10").place(x = 105, y = 80) 

lblModifyUser = Label(usuariosTab, text="Ingrese permisos nuevos si desea modificar o crear").place(x = 10, y = 120)

btnCreateUser = Button(usuariosTab, text="Crear", command=crearUsuario, width="10").place(x = 180, y = 150) 
btnModifyUser = Button(usuariosTab, text="Modificar", command=modificarUsuario, width="10").place(x = 180, y = 190) 
btnSalirUsuariosAdm = Button(usuariosTab, text="Salir", command=lambda: salir(mainMenu,winLogin), width="10").place(x = 180, y = 230) 

rbn1 = Radiobutton(usuariosTab, text='Lector', variable=tipoUserAdm, value='lector')
rbn1.place(x=20, y=155)
rbn2 = Radiobutton(usuariosTab, text='Escritor', variable=tipoUserAdm, value='escritor')
rbn2.place(x=20, y=180)
rbn3 = Radiobutton(usuariosTab, text='Versatil', variable=tipoUserAdm, value='versatil')
rbn3.place(x=20, y=205)
rbn4 = Radiobutton(usuariosTab, text='Admin', variable=tipoUserAdm, value='admin')
rbn4.place(x=20, y=230)

entryComicBuscado.bind("<Return>", buscarComic)
lbSugerencias.bind("<Double-Button-1>", leerComic)

#-------------------CREAR TAB------------------
nomCrear = StringVar()
numeroCrear = StringVar()
escritorCrear = StringVar()
dibujanteCrear = StringVar()
portadaCrear = StringVar()
publicacionCrear = StringVar()
imagenCrear = StringVar()

lblInfoGeneralCrear = Label(crearTab, text="Información general del Cómic").place(x = 60, y = 5)

lblNomCrear = Label(crearTab, text="Nombre del Cómic").place(x = 20, y = 25)
entryNomCrear = Entry(crearTab, textvariable=nomCrear)
entryNomCrear.place(x = 10, y = 45)

lblNumeroCrear = Label(crearTab, text="# de edición").place(x = 35, y = 65)
entryNumeroCrear = Entry(crearTab, textvariable=numeroCrear)
entryNumeroCrear.place(x = 10, y = 85)

lblEscritorCrear = Label(crearTab, text="Escritor").place(x = 47, y = 105)
entryEscritorCrear = Entry(crearTab, textvariable=escritorCrear)
entryEscritorCrear.place(x = 10, y = 125)

lblDibujanterCrear = Label(crearTab, text="Dibujante").place(x = 42, y = 145)
entryDibujanteCrear = Entry(crearTab, textvariable=dibujanteCrear)
entryDibujanteCrear.place(x = 10, y = 165)

lblPortadaCrear = Label(crearTab, text="Creador Portada").place(x = 25, y = 185)
entryPortadaCrear = Entry(crearTab, textvariable=portadaCrear)
entryPortadaCrear.place(x = 10, y = 205)

lblPublicacionCrear = Label(crearTab, text="Fecha Publicación").place(x = 20, y = 225)
entryPublicacionCrear = Entry(crearTab, textvariable=publicacionCrear)
entryPublicacionCrear.place(x = 10, y = 245)

lblImagenCrear = Label(crearTab, text="Imagen Portada").place(x = 170, y = 25)
entryImagenCrear = Entry(crearTab, textvariable=imagenCrear)
entryImagenCrear.place(x = 150, y = 45)

lblSinopsisCrear = Label(crearTab, text="Sinopsis").place(x = 190, y = 65)
txtAreaSinopsisCrear = Text(crearTab, width=15, height=9)
scrollbarCrear = Scrollbar(crearTab, command=txtAreaSinopsisCrear.yview)
scrollbarCrear.pack(side=RIGHT, fill=Y)
txtAreaSinopsisCrear.config(yscrollcommand=scrollbarCrear.set)
txtAreaSinopsisCrear.place(x = 150, y = 85)

btnIniciarCrear = Button(crearTab, text="Iniciar", command=iniciarCreacion, width="7").place(x = 150, y = 240) 
btnSalirCrear = Button(crearTab, text="Salir", command=lambda: salir(mainMenu,winLogin), width="7").place(x = 215, y = 240) 

txtAreaSinopsisCrear.bind("<Return>", iniciarCreacion)

#-------------------WIN CREANDO------------------
imagenPaginaCreando = StringVar()
imagenCreando = StringVar()
personajeCreando = StringVar()

numDiaCreando = StringVar()
numEscCreando = StringVar()
numPagCreando = StringVar()

lblImagenPaginaCreando = Label(winCrear, text="Imagen página completa").place(x = 10, y = 10)
entryImagenPaginaCreando = Entry(winCrear, textvariable=imagenPaginaCreando, width=20)
entryImagenPaginaCreando.place(x =155, y = 13)

lblImagenCreando = Label(winCrear, text="Imagen de escena").place(x = 30, y = 40)
entryImagenCreando = Entry(winCrear, textvariable=imagenCreando)
entryImagenCreando.place(x =20, y = 60)

lblTextoCreando = Label(winCrear, text="Texto").place(x = 60, y = 80)
txtAreaTextoCreando = Text(winCrear, width=15, height=8)
scrollbarCreando = Scrollbar(winCrear, command=txtAreaTextoCreando.yview)
scrollbarCreando.pack(side=RIGHT, fill=Y)
txtAreaTextoCreando.config(yscrollcommand=scrollbarCreando.set)
txtAreaTextoCreando.place(x = 20, y = 100)

lblPersonajeCreando = Label(winCrear, text="Personaje").place(x = 50, y = 230)
entryPersonajeCreando = Entry(winCrear, textvariable=personajeCreando)
entryPersonajeCreando.place(x =20, y = 250)

lblPaginaCreando = Label(winCrear, text="Página: ").place(x = 170, y = 40)
lblEscenaCreando = Label(winCrear, text="Escena:").place(x = 170, y = 60)
lblDialogoCreando = Label(winCrear, text="Dialogo:").place(x = 170, y = 80)

lblNumPagCreando = Label(winCrear,textvariable = numPagCreando, text="").place(x = 250, y = 40)
lblNumEscCreando = Label(winCrear,textvariable = numEscCreando, text="").place(x = 250, y = 60)
lblNumDiaCreando = Label(winCrear,textvariable = numDiaCreando, text="").place(x = 250, y = 80)

btnInsertarDialogo = Button(winCrear, text="Insertar Dialogo", command=insertarDialogo, width="15").place(x = 160, y = 110) 
btnInsertarEscena = Button(winCrear, text="Insertar Escena", command=insertarEscena, width="15").place(x = 160, y = 140) 
btnInsertarPagina = Button(winCrear, text="Insertar Pagina", command=insertarPagina, width="15").place(x = 160, y = 170) 
btnInsertarComic = Button(winCrear, text="Finalizar Cómic", command=insertarComic, width="15").place(x = 160, y = 200) 

btnSalirCreaando = Button(winCrear, text="Salir", command=lambda: salir(winCrear,mainMenu),width="10").place(x = 195, y = 245) 

#-------------------EDITAR TAB------------------

btnEditarPersonaje = Button(editarTab, text="Editar Personajes", command=lambda: salir(mainMenu,winEditarPerso), width="15").place(x = 160, y = 35)


inputComicBuscadoEditC = StringVar()

modoEdicion = StringVar(value='Paginas')

lblEditarComic = Label(editarTab, text="Editar Comic").place(x = 40, y = 10)


entryComicBuscadoEditC = Entry(editarTab, textvariable=inputComicBuscadoEditC)
entryComicBuscadoEditC.place(x = 20, y = 40)

lbSugerenciasEditC = Listbox(editarTab, height=10)
lbSugerenciasEditC.place(x = 20, y = 70)

rbn3EditC = Radiobutton(editarTab, text='Editar Paginas', variable=modoEdicion, value='Paginas')
rbn3EditC.place(x=170, y=70)
rbn2EditC = Radiobutton(editarTab, text='Editar Escenas', variable=modoEdicion, value='Escenas')
rbn2EditC.place(x=170, y=90)
rbn1EditC = Radiobutton(editarTab, text='Editar Dialogos', variable=modoEdicion, value='Dialogos')
rbn1EditC.place(x=170, y=110)


btnEliminarEditarComic = Button(editarTab, text="Editar Cómic", command=editarComic, width="15").place(x = 160, y = 150) 

btnEditarComic = Button(editarTab, text="Eliminar", command=eliminarComic, width="15").place(x = 160, y = 180) 

btnSalirEditarTab = Button(editarTab, text="Salir", command=lambda: salir(mainMenu,winLogin), width="15").place(x = 160, y = 210) 

entryComicBuscadoEditC.bind("<Return>", buscarComicEditarC)


#------------------WIN EDITAR COMIC-------------
persoSelecEditC = StringVar()
posSelecEditC = StringVar()
posMaximaNum = StringVar()
numPagEditando = StringVar()
numEscEditando = StringVar()
numDiaEditando = StringVar()
personajeLableEditC = StringVar(value='Personaje')
btnAnteriorEditando= Button(winEditarComic, text="Anterior", command=lambda: tipoEdicion('Anterior'), width="10").place(x = 205, y = 70) 

btnSiguienteEditando = Button(winEditarComic, text="Siguiente", command=lambda: tipoEdicion('Siguiente'), width="10").place(x = 295, y = 70) 

lblTituloModoEdicion = Label(winEditarComic, text="",textvariable=modoEdicion).place(x = 170, y = 10)
lblDialogosEditC = Label(winEditarComic, text="Texto").place(x = 80, y = 40)

txtAreaDiaSelecEditC = Text(winEditarComic, width=22, height=13)
txtAreaDiaSelecEditC.place(x = 10, y = 60)

lblPersonajeEditC = Label(winEditarComic,textvariable=personajeLableEditC)
lblPersonajeEditC.place(x = 72, y = 280)

entryPersoSelecEditC = Entry(winEditarComic, textvariable=persoSelecEditC, width=30)
entryPersoSelecEditC.place(x = 10, y = 300)

lblPosicionEditC = Label(winEditarComic, text="Posición").place(x = 72, y = 330)

entryPosSelecEditC = Entry(winEditarComic, textvariable=posSelecEditC, width=30)
entryPosSelecEditC.place(x = 10, y = 350)

lblDiaEditando= Label(winEditarComic, text="Dia:")
lblDiaEditando.place(x = 320, y = 130)

lblDiaNumEditando= Label(winEditarComic, textvariable=numDiaEditando)
lblDiaNumEditando.place(x = 350, y = 130)

lblEscEditando= Label(winEditarComic, text="Esc:")
lblEscEditando.place(x = 260, y = 130)

lblEscNumEditando= Label(winEditarComic, textvariable=numEscEditando)
lblEscNumEditando.place(x = 290, y = 130)

lblPagEditando= Label(winEditarComic, text="Pag:")
lblPagEditando.place(x = 200, y = 130)

lblPagNumEditando= Label(winEditarComic, textvariable=numPagEditando)
lblPagNumEditando.place(x = 230, y = 130)


lblPosMax = Label(winEditarComic, text="Posición Max Disponible:").place(x = 200, y = 180)

lblPosMaxNum= Label(winEditarComic, textvariable=posMaximaNum).place(x = 360, y = 180)

lblPosMin = Label(winEditarComic, text="Posición Min Disponible:").place(x = 200, y = 210)

lblNumUno = Label(winEditarComic, text="1").place(x = 360, y = 210)

btnEliminarEditando= Button(winEditarComic, text="Editar", command=atualizaComicEditC, width="20").place(x = 220, y = 270) 

btnActualizarEditando = Button(winEditarComic, text="Eliminar", command=eliminarParte, width="20").place(x = 220, y = 310) 

btnSalirEditando = Button(winEditarComic, text="Salir", command=lambda: salir(winEditarComic,mainMenu), width="20").place(x = 220, y = 350) 

#------------------WIN EDITAR PERSO-------------
persoBuscadoEdit = StringVar() 

personajeEditP = StringVar()
nombreEditP = StringVar()
nacimientoEditP = StringVar()
origenEditP = StringVar()
resideEditP = StringVar()
afiliacionesEditP = StringVar()
habilidadesEditP = StringVar()
amorEditP = StringVar()
creadorEditP = StringVar()
aliadosEditP = StringVar()
enemigosEditP = StringVar()

lblPersoBuscadoEdit = Label(winEditarPerso, text="Buscar Personaje").place(x = 55, y = 10)

entryPersoBuscadoEdit= Entry(winEditarPerso, textvariable=persoBuscadoEdit, width=27)
entryPersoBuscadoEdit.place(x = 20, y = 30)

lbPersoBuscadoEdit = Listbox(winEditarPerso, width=27)
lbPersoBuscadoEdit.place(x = 20, y = 65)

btnBuscarPersoEditar = Button(winEditarPerso, text="Buscar", command=buscarPersoEditar, width="15").place(x = 45, y = 235)
entryPersoBuscadoEdit.bind("<Return>", buscarPersoEditar)
lbPersoBuscadoEdit.bind("<Double-Button-1>", seleccionarEditP)

lblPersonajeEditP = Label(winEditarPerso, text="Personaje").place(x = 75, y = 270)
entryPersonajeEditP = Entry(winEditarPerso, textvariable=personajeEditP, width=27)
entryPersonajeEditP.place(x = 20, y = 290)

lblNombreEditP = Label(winEditarPerso, text = "Nombre").place(x = 77, y = 310)
entryNombreEditP = Entry(winEditarPerso, textvariable=nombreEditP, width=27)
entryNombreEditP.place(x = 20, y = 330)

lblNacimientoEditP = Label(winEditarPerso, text = "Nacimiento").place(x = 70, y = 350)
entryNacimientoEditP = Entry(winEditarPerso, textvariable=nacimientoEditP, width=27)
entryNacimientoEditP.place(x = 20, y = 370)

lblOrigenEditP = Label(winEditarPerso, text = "Origen").place(x = 80, y = 390)
entryOrigenEditP = Entry(winEditarPerso, textvariable=origenEditP, width=27)
entryOrigenEditP.place(x = 20, y = 410)

lblResideEditP = Label(winEditarPerso, text = "Reside").place(x = 80, y = 430)
entryResideEditP = Entry(winEditarPerso, textvariable=resideEditP, width=27)
entryResideEditP.place(x = 20, y = 450)

lblAfiliacionesEditP = Label(winEditarPerso, text="Afiliaciones").place(x = 315, y = 10)
entryAfiliacionesEditP = Entry(winEditarPerso, textvariable=afiliacionesEditP, width=45)
entryAfiliacionesEditP.place(x = 210, y = 30)

lblHabilidadesEditP = Label(winEditarPerso, text = "Habilidades").place(x = 315, y = 50)
entryHabilidadesEditP = Entry(winEditarPerso, textvariable=habilidadesEditP, width=45)
entryHabilidadesEditP.place(x = 210, y = 70)

lblAmorEditP = Label(winEditarPerso, text = "Amor").place(x = 328, y = 90)
entryAmorEditP = Entry(winEditarPerso, textvariable=amorEditP, width=45)
entryAmorEditP.place(x = 210, y = 110)

lblCreadorEditP = Label(winEditarPerso, text = "Creador").place(x = 323, y = 130)
entryCreadorEditP = Entry(winEditarPerso, textvariable=creadorEditP, width=45)
entryCreadorEditP.place(x = 210, y = 150)

lblEnemigosEditP = Label(winEditarPerso, text = "Enemigos").place(x = 320, y = 170)
entryEnemigosEditP = Entry(winEditarPerso, textvariable=enemigosEditP, width=45)
entryEnemigosEditP.place(x = 210, y = 190)

lblAliadosEditP = Label(winEditarPerso, text="Aliados").place(x = 325, y = 210)
entryAliadosEditP = Entry(winEditarPerso, textvariable=aliadosEditP, width=45)
entryAliadosEditP.place(x = 210, y = 230)

lblHistoriaEditP = Label(winEditarPerso, text = "Historia").place(x = 325, y = 250)
txtAreaHistoriaEditP = Text(winEditarPerso, width=34, height=5)
txtAreaHistoriaEditP.place(x = 210, y = 270)

btnBuscarPersoEditar = Button(winEditarPerso, text="Actualizar", command=modificarPersonaje, width="35").place(x = 220, y = 370)

btnBuscarPersoEditar = Button(winEditarPerso, text="Borrar", command=eliminarPersonaje, width="35").place(x = 220, y = 405)

btnBuscarPersoEditar = Button(winEditarPerso, text="Salir",  command=lambda: salir(winEditarPerso,mainMenu), width="35").place(x = 220, y = 440)
#endregion
mainloop()