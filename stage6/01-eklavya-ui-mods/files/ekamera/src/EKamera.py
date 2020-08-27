#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Interface graphique

import tkinter as tk
from tkinter import (messagebox, Frame, Label, Entry, Button, LabelFrame, Canvas,
PhotoImage, Spinbox, Listbox, StringVar, Menu, Scale, Scrollbar, BooleanVar, Checkbutton, Tk, filedialog)
from CallTipWindow import createToolTip
from time import strftime, localtime
from fractions import Fraction
from picamera import PiCamera


# Options de la caméra à l'ouverture
IMAGE_WIDTH = int(1280/2)
IMAGE_HEIGHT = int(720/2)
RESOLUTION_PREVIEW = (IMAGE_WIDTH, IMAGE_HEIGHT)
RESOLUTION_CAMERA = (1280, 720)

# Options de l'interface
SIZE_OPTIONS = 400
BD = 2

# Répertoires
CAPTURE_DIR = '/home/pi/Pictures/'
VIDEO_DIR = '/home/pi/Videos/'
IMAGE_DIR = '/etc/eklavya/ekamera/images/'


class EKamera(Frame):

    # Constructor
    def __init__(self, root, camera, title):

        """
        Initializes window, camera settings, sub-windows and widgets, preview,
        event management and other attributes useful for the operation of the application

        """

        # Initialisation de la fenêtre
        self.mainFrame = Frame.__init__(self, root)
        self.root = root
        self.title = title
        self.root.title(title)
        self.grid()

        # Initialisation de la caméra
        self.camera = camera
        self.resolution = RESOLUTION_CAMERA
        self.camera.resolution = self.resolution
        self.camera.framerate = 24
        self.etatCapture = ["Ready to capture", ""]
        self.dernierFichier = ""
        self.video_dir = VIDEO_DIR
        self.photo_dir = CAPTURE_DIR

        # Initializing Panels and Buttons
        self.createFrames()
        self.createLabelFrames()
        self.createWidgets()

        # Initializing the preview
        self.pos_preview = self.posPreview()
        self.resPreview = RESOLUTION_PREVIEW
        self.winPreview = (self.pos_preview[0], self.pos_preview[1],
                           self.resPreview[0], self.resPreview[1])
        self.camera.start_preview(fullscreen=False, window=self.winPreview)

        # Other
        self.hflip = False
        self.vflip = False
        self.i = 0
        self.format = 'png'
        self.nomFichier = 'capture'
        self.champ = 'Done'
        self.angle = 0
        self.recording = False

        # Initialization of event management
        self.createBindings()


    # Destructor
    def __del__(self):

        """
        S'assure d'effacer l'instance de ``PiCamera`` pour éviter des problèmes de mémoire

        """

        self.camera.stop_preview()
        del self.camera


    """
    Cette section contient tout ce qui rapporte à la création de l'interface, c'est-à-dire
    Les fenêtres, les sous-fenêtres d'options, les sous-fenêtres d'aperçu et la barre de menu

    """


    def createFrames(self):

        """
        Crée les sous-fenêtres

        """

        # Crée la sous-fenêtre virtuelle de la section des aperçus
        self.sectionFrame = Frame(self.root)
        self.sectionFrame.grid(row=0, column=1)

        # Crée la sous-fenêtre de l'aperçu
        self.imageFrame = LabelFrame(self.sectionFrame, text = "Preview", width=IMAGE_WIDTH+5, height=IMAGE_HEIGHT+5,bd=BD)
        self.imageFrame.grid(row=0, column=1)
        self.previewFrame = Frame(self.imageFrame, width=IMAGE_WIDTH, height=IMAGE_HEIGHT, bd=BD, bg='black')
        self.previewFrame.grid()

        # Crée la sous-fenêtre de l'aperçu de la capture
        self.captureFrame = LabelFrame(self.sectionFrame, text = "Capture",
                                          width=IMAGE_WIDTH+2, height=IMAGE_HEIGHT+2,bd=BD)
        self.captureFrame.grid(row=1, column=1)
        self.captureCanvas = Canvas(self.captureFrame, width=IMAGE_WIDTH, height=IMAGE_HEIGHT,bd=BD, cursor="tcross")
        self.imagedefaut = PhotoImage(file=IMAGE_DIR+"eklavya_default.png")
        #self.imagedefaut = self.imagedefaut.zoom(1)
        self.imagedefaut = self.imagedefaut.subsample(3)
        self.captureCanvas.create_image(0,0,image=self.imagedefaut, anchor='nw')
        self.captureCanvas.grid()

        # Crée la sous-fenêtre des options
        self.optionsFrame = LabelFrame(self.sectionFrame, text = "Options", width=SIZE_OPTIONS, height=IMAGE_HEIGHT, bd=BD)
        self.optionsFrame.grid(row=0, column=0, rowspan=3, pady=4)

        # Crée la sous-fenêtre virtuelle des commandes
        self.commandesFrame = Frame(self.sectionFrame)
        self.commandesFrame.grid(row=2, column=1)

        # Crée la sous-fenêtre des commandes
        self.buttonsFrame = LabelFrame(self.commandesFrame, text = "Commands", width=IMAGE_WIDTH/2, height=50, bd=BD)
        self.buttonsFrame.grid(row=2, column=1)

        bsize = self.get_cmdsize()
        # Crée la sous-fenêtre des options de la capture en séquence
        self.optionseqFrame = LabelFrame(self.commandesFrame, text = "Sequence",width=bsize[0]-10, height=bsize[1], bd=BD)
        self.optionseqFrame.grid(row=2, column=0,sticky='w')
        self.optionseqFrame.grid_propagate(0)

        # Crée la sous-fenêtre de l'état de la capture
        self.etatFrame = LabelFrame(self.commandesFrame, text = "State",width=bsize[0]+10, height=bsize[1], bd=BD)
        self.etatFrame.grid(row=2, column=3,sticky='e')
        self.etatFrame.grid_propagate(0)


    def createLabelFrames(self):

        """
        Crée les sous-fenêtres des options

        """

        # Division des fenêtres
        div = 1.75

        # Sous-fenêtre de l'option Image
        self.image_Frame = LabelFrame(self.optionsFrame, text = "Image", width = SIZE_OPTIONS, height = int(IMAGE_HEIGHT/div)+10, bd=BD)
        self.image_Frame.grid(row=0)
        self.image_Frame.grid_propagate(0)  # Empêche la déformation de la fenêtre
        self.createImage()  # Initialise les widgets

        # Sous-fenêtre de l'option Résolution
        self.resFrame = LabelFrame(self.optionsFrame, text = "Resolution", width = SIZE_OPTIONS, height = int(IMAGE_HEIGHT/div)+50-10, bd=BD)
        self.resFrame.grid(row=1)
        self.resFrame.grid_propagate(0)
        self.createRes()

        # Sous-fenêtre de l'option Texte
        self.textFrame = LabelFrame(self.optionsFrame, text = "Text", width = SIZE_OPTIONS, height = int(IMAGE_HEIGHT/div)-50-10, bd=BD)
        self.textFrame.grid(row=2)
        self.textFrame.grid_propagate(0)
        self.createText()

        # Sous-fenêtre de l'option Sauvegarder
        self.saveFrame = LabelFrame(self.optionsFrame, text="Save As", width = SIZE_OPTIONS, height = int(IMAGE_HEIGHT/div)+10, bd=BD)
        self.saveFrame.grid(row=3)
        self.saveFrame.grid_propagate(0)
        self.createSave()


    def createMenu(self):

        """
        Crée la barre de menu

        """

        # Crée un menu virtuel
        self.menubar = Menu(self)

        # crée le menu Fichier et l'attache au menu virtuel
        menuFichier=Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menuFichier)
        menuFichier.add_command(label="Photo Directory", command=self.changerRepertoirePhoto)
        menuFichier.add_command(label="Video Directory", command=self.changerRepertoireVideo)
        menuFichier.add_command(label="Reset", command=self.reset_all)
        menuFichier.add_command(label="Exit", command=self.quit)

        # crée le menu Éditer et l'attache au menu virtuel
        menuEditer = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=menuEditer)
        menuEditer.add_command(label="Rotate horizontal", command=self.hflip)
        menuEditer.add_command(label="Rotate vertical", command=self.vflip)
        menuEditer.add_command(label="Rotate", command=self.rotate)

        # crée le menu Capture et l'attache au menu virtuel
        menuCapture = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Capture", menu=menuCapture)
        menuCapture.add_command(label="Photo", command=self.capture)
        menuCapture.add_command(label="Video", command=self.recVideo)
        menuCapture.add_command(label="Sequence", command=self.captureSeq)

        # crée le menu Aide et l'attache au menu virtuel
        menuAide = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=menuAide)
        menuAide.add_command(label="About", command=self.createAide)

        # Affiche le menu
        self.master.config(menu=self.menubar)


    def createImage(self):

        """
        Crée la sous-fenêtre ``Image`` et initialise les widgets de celle-ci

        """

        # Crée l'emplacement de la glissoire de zoom
        self.zoom_Frame=Frame(self.image_Frame)
        self.zoom_Frame.grid(row=0, column=0, sticky='w')
        Label(self.zoom_Frame, text='Zoom').grid(row=0,column=0,sticky='w')
        # Crée la glissoire du zoom
        self.zoomScale = Scale(self.zoom_Frame, from_=0, to =100, orient="horizontal")
        self.zoomScale.grid(row=1,column=0,sticky='w')

        # Crée la sous-fenêtre virtuelle pour placer les glissoires de déplacement
        self.deplacementFrame = Frame(self.zoom_Frame)
        self.deplacementFrame.grid(row=2,sticky='w')

        # Crée la glissoire du déplacement en X
        Label(self.deplacementFrame, text='Move').grid(row=0,columnspan=2,sticky='w')
        Label(self.deplacementFrame, text='X').grid(row=1,column=0,sticky='s')
        self.xzoomScale = Scale(self.deplacementFrame, from_=0, to =100, orient="horizontal")
        self.xzoomScale.grid(row=1,column=1,sticky='w')
        self.xzoomScale.set(50)

        # Crée la glissoire du déplacement en X
        Label(self.deplacementFrame, text='Y').grid(row=2,column=0,sticky='s')
        self.yzoomScale = Scale(self.deplacementFrame, from_=0, to =100, orient="horizontal")
        self.yzoomScale.grid(row=2,column=1,sticky='w')
        self.yzoomScale.set(50)

        # Crée le bouton de réinitialisation du zoom
        self.resetFrame = Frame(self.zoom_Frame)
        self.resetFrame.grid(row=3, column=0)
        self.resetButton = Button(self.resetFrame, text='Reset', command=self.reset_size)
        self.resetButton.grid()

        Label(self.image_Frame, text='      ').grid(row=0,column=1,sticky='w')

        # Crée la section pour placer les options de l'exposition
        self.expFrame = Frame(self.image_Frame)
        self.expFrame.grid(row=0, column=2,sticky="n")
        Label(self.expFrame, text='Exposure (Auto: 0)').grid(row=0,column=0,columnspan=2,sticky='nw')

        # Crée la glissoire de l'ISO
        Label(self.expFrame, text='ISO', justify='left').grid(row=1,column=0,sticky='w')
        self.isoScale = Scale(self.expFrame, from_=0, to =1600, orient="horizontal")
        self.isoScale.grid(row=1,column=1,sticky='w')

        # Crée la glissoire du shutter speed
        Label(self.expFrame, text='Shutter\nspeed', justify='left').grid(row=2,column=0,sticky='w')
        self.shutterScale = Scale(self.expFrame, from_=0, to =40000, orient="horizontal")
        self.shutterScale.grid(row=2,column=1,sticky='w')

        # Crée la barre de défilement des modes d'exposition
        scrollbar = Scrollbar(self.expFrame, orient="vertical")

        # Liste des modes d'exposition
        self.list_exp = ["off", "auto", "night", "nightpreview", "blacklight", "spotlight", "sports", "snow", "beach", "very long", "fixedfps", "antishake", "fireworks"]
        self.modeLabel = Label(self.expFrame, text="Exposure Modes", justify='left')
        self.modeLabel.grid(row=4, column=0, sticky='nw')

        # Initialise la boîte des résolutions par défaut et assigne la barre de défilement à celle-ci
        self.expListbox = Listbox(self.expFrame, height=3, width=13, yscrollcommand=scrollbar.set)

        scrollbar.grid(column=2, row=4, sticky='w'+'n'+'s')
        scrollbar.config(command=self.expListbox.yview)

        # Place les éléments de la liste des résolutions par défaut dans la boîte
        for item in self.list_exp:
            self.expListbox.insert("end", item)
        self.expListbox.grid(row=4, column=1)
        self.expListbox.activate(1)  # Active par défaut le mode "auto"

        # Crée le bouton confirmer la résolution par défaut
        Button(self.expFrame, text="Confirm", command=self.set_expmode).grid(row=5, columnspan=2, column=1)

        # Crée le tooltip qui s'affichera au dessus du texte "Modes d'exposition"
        note = "Activate an exposure mode\nprevent manual configuration\nISO and shutter speed"
        createToolTip(self.modeLabel, note)


    def createRes(self):

        """
        Crée la sous-fenêtre ``Résolution`` et initialise les widgets de celle-ci

        """

        self.resdefFrame = Frame(self.resFrame)
        self.resdefFrame.grid(row=0, sticky='w')

        # Crée la barre de défilement des résolution par défaut
        scrollbar = Scrollbar(self.resdefFrame, orient="vertical")

        # Liste des résolutions par défaut: (WIDTH, HEIGHT, "ASPECT RATIO", CAMERA_MODE, "CHAMP DE VISION")
        self.list_res = [(2592, 1944, "4:3", 2, "Full"),
                         (1920, 1080, "16:9", 1, "Partial"),
                         (1296, 974, "4:3", 4, "Full"),
                         (1296, 730, "16:9", 5, "Full"),
                         (640, 480, "4:3", 7, "Partial")]
        Label(self.resdefFrame, text='Default resolutions').grid(row=0, column=0,sticky='w')

        # Initialise la boîte des résolutions par défaut et assigne la barre de défilement à celle-ci
        self.resListbox = Listbox(self.resdefFrame, height=3, width=22, yscrollcommand=scrollbar.set)

        scrollbar.grid(column=1, row=1, sticky='w'+'n'+'s')
        scrollbar.config(command=self.resListbox.yview)

        # Place les éléments de la liste des résolutions par défaut dans la boîte
        for item in self.list_res:
            self.resListbox.insert("end", "{}x{} ({}, {})".format(item[0],item[1], item[2], item[4]))
        self.resListbox.grid(row=1, column=0)
        self.resListbox.activate(4)  # Active par défaut la résolution 1296x730

        # Crée le bouton confirmer la résolution par défaut
        self.confirmdefButton = Button(self.resFrame, text="Confirm", command=self.set_resdef)
        self.confirmdefButton.grid(row=1)

        # Variable de résolution personnalisée
        self.resPersoW = StringVar()
        self.resPersoH = StringVar()

        self.tailleFrame = Frame(self.resFrame)
        self.tailleFrame.grid(row=2,sticky='w')

        # Crée la boîte d'entrée de l'utilisateur pour la largeur et la hauteur de l'image
        Label(self.tailleFrame, text="Custom Resolution").grid(row=0, column=0, columnspan=2, sticky='w')
        Label(self.tailleFrame, text="Width:").grid(row=1, column=0,sticky='w')
        self.largeurEntry = Entry(self.tailleFrame, textvariable=self.resPersoW, validate="focusout", validatecommand=self.verify_resW)
        self.largeurEntry.grid(row=1, column=1,sticky='w')
        Label(self.tailleFrame, text="Height:").grid(row=2, column=0,sticky='w')
        self.hauteurEntry = Entry(self.tailleFrame, textvariable=self.resPersoH, validate="focusout", validatecommand=self.verify_resH)
        self.hauteurEntry.grid(row=2, column=1,sticky='w')

        # Crée un tooltip relié au frame self.tailleFrame
        note="Minimum: 64x64 px"+"\n"+"Maximum: 2592x1944 px"
        createToolTip(self.tailleFrame, note)

        # Crée le bouton confirmer la résolution personnalisée
        self.confirmButton = Button(self.resFrame, text="Confirm", command=self.set_res)
        self.confirmButton.grid(row=3)

        # Crée l'emplacement de l'aperçu de la résolution actuelle et du champ de vision actuel
        self.resactuelleFrame = Frame(self.resFrame)
        self.resactuelleFrame.grid(row=4, sticky='w')
        self.resactuelleLabel = Label(self.resactuelleFrame, text="Actual Resolution: {}x{}".format(self.resolution[0], self.resolution[1]))
        self.resactuelleLabel.grid(row=0)
        self.champLabel = Label(self.resactuelleFrame, text='Field of view: Partial')
        self.champLabel.grid(row=1, sticky='w')


    def createText(self):

        """
	Crée la sous-fenêtre ``Texte`` et initialise les widgets de celle-ci

	"""

        self.annoterTemps = BooleanVar(False)  # Annoter le temps (Bool)
        self.textVar = StringVar("")  # Texte personnalisé (String)

        # String qui dit le temps sous la forme (Année - Mois - Jour - Heure : Minute : Seconde)
        self.temps = strftime("%Y-%m-%d-%H:%M:%S" , localtime())

        self.tempsFrame = Frame(self.textFrame)
        self.tempsFrame.grid(row=0,sticky='w')
        Label(self.tempsFrame, text="Annotate the time to the photo").grid(row=0,column=0)

        # Crée le bouton qui contrôle si le temps s'affiche sur la photo
        self.tempsButton = Checkbutton(self.tempsFrame, variable=self.annoterTemps, command=self.set_overlayText)
        self.tempsButton.grid(row=0, column=1, sticky="w")

        # Exemple du temps qui sera affiché
        self.tempsLabel = Label(self.tempsFrame, text=self.temps)
        self.tempsLabel.grid(row=1,column=0, sticky='w')

        # Actualise le temps à afficher dans l'exemple
        self.update_temps(False)

        Label(self.textFrame, text="  ").grid(row=1)
        self.persoFrame = Frame(self.textFrame)
        self.persoFrame.grid(row=2,sticky='w')
        Label(self.persoFrame, text="Customize :").grid(row=0, column=0, sticky='w')

        # Crée la boîte d'entrée de l'utilisateur pour le texte personnalisé à afficher
        self.textEntry = Entry(self.persoFrame, textvariable=self.textVar)
        self.textEntry.grid(row=0,column=1, sticky='w')

        # Crée un tooltip relié au label "Personnalisé"
        note="N'does not accept special characters"+"\n"+"(ASCII code less than 128)"
        createToolTip(self.textEntry, note)


    def createSave(self):

        """
        Crée la sous-fenêtre ``Sauvegarder`` et initialise les widgets de celle-ci

        """

        self.fichierVar = StringVar()  # Nom du fichier (String)

        self.fichierFrame = Frame(self.saveFrame)
        self.fichierFrame.grid(row=0,sticky='w')
        Label(self.fichierFrame, text='File format:').grid(row=0, column=0,sticky='w')

        # Crée la boîte déroulante du format de la photo à enregistrer
        self.formatSpinbox = Spinbox(self.fichierFrame, values=("png","jpg", "gif","bmp","rgb","rgba"), width=5)
        self.formatSpinbox.grid(row=0, column=1,sticky='w')

        # Crée un tooltip relié à la spinbox du format
        note = "The format of the video files\nis .h264 as default."
        createToolTip(self.formatSpinbox, note)

        # Crée la boîte d'entrée de l'utilisateur pour le nom du fichier
        Label(self.fichierFrame, text='File name:').grid(row=1, column=0,sticky='w')
        self.fichierEntry = Entry(self.fichierFrame, textvariable=self.fichierVar)
        self.fichierEntry.grid(row=1, column=1,sticky='w')
        Button(self.saveFrame, text="Confirm", command=self.update_nomFichier).grid(row=1)

        # Aperçu du nom de fichier photo
        self.apercuFichierphoto = Label(self.saveFrame, text="Photo File: capture.png")
        self.apercuFichierphoto.grid(row=4, sticky='w')

        # Aperçu du nom de fichier vidéo
        self.apercuFichiervideo = Label(self.saveFrame, text="Video File: capture.h264")
        self.apercuFichiervideo.grid(row=5, sticky='w')

        Label(self.saveFrame, text='').grid(row=6,sticky='w')

        # Aperçu du répertoire photo
        self.apercuRepertoirephoto = Label(self.saveFrame, text="Photo directory: " + self.photo_dir)
        self.apercuRepertoirephoto.grid(row=7, sticky='w')

        # Aperçu du répertoire vidéo
        self.apercuRepertoirevideo = Label(self.saveFrame, text="Video directory: " + self.video_dir)
        self.apercuRepertoirevideo.grid(row=8, sticky='w')


    def createAide(self):

        """
	Crée une fenêtre indiquant les informations relatives au logiciel

	"""
        self.aide = Tk()
        self.aide.title("About")
        self.aideFrame = Frame(self.aide)
        self.aideFrame.grid()
        Label(self.aideFrame, text="Réal Paquin\nJérémy Talbot-Pâquet\nUniversité Laval - 2018\nSudeep Hazra 2020").grid()
        self.centrerAide()


    """
    Cette section contient les commandes des widgets et la fonction qui initialise les boutons de commande

    """


    def createWidgets(self):

        """
	Crée les boutons de l'interface des commandes et la barre de menu

	"""
        # Crée le bouton capture
        # Ajuste la taille de l'image du bouton capture
        self.cameraPNG=PhotoImage(file=IMAGE_DIR+"camera.png")
        self.cameraPNG=self.cameraPNG.subsample(7)
        self.photoButton = Button(self.buttonsFrame, image=self.cameraPNG,
                                    width="40",height="40",
            command=self.capture)
        self.photoButton.grid(column=2, row=0)

        # Crée le bouton capture séquence
        # Ajuste la taille de l'image du bouton capture séquence
        self.seqPNG=PhotoImage(file=IMAGE_DIR+"burst-shot.png")
        #self.seqPNG=self.seqPNG.zoom(10)
        self.seqPNG=self.seqPNG.subsample(7)
        self.seqButton = Button(self.buttonsFrame, image=self.seqPNG,
                                    width="40",height="40",
            command=self.captureSeq)
        self.seqButton.grid(column=1, row=0)

        # Crée le bouton capture séquence
        # Ajuste la taille de l'image du bouton capture séquence
        self.videoPNG=PhotoImage(file=IMAGE_DIR+"video.png")
        #self.videoPNG=self.videoPNG.zoom(10)
        self.videoPNG=self.videoPNG.subsample(7)
        self.videoButton = Button(self.buttonsFrame, image=self.videoPNG,
                                    width="40",height="40",
            command=self.recVideo)
        self.videoButton.grid(column=3, row=0)

        # Crée la spinbox pour le nombre de captures en séquence
        Label(self.optionseqFrame, text="Photos: ").grid(column=0,row=0,sticky='w')
        self.seqSpinbox = Spinbox(self.optionseqFrame, values=(2,3,4,5,6,8,10,12,15,20),width=8)
        self.seqSpinbox.grid(column=1,row=0,sticky='w')
        self.nbseq = self.seqSpinbox.get()

        # Crée le canvas pour afficher l'état de l'application
        self.etatCanvas = Canvas(self.buttonsFrame, width=40, height=40)
        self.etatCanvas.grid(column=5, row=0)

        # Crée le bouton de revirement horiztonal
        # Ajuste la taille de l'image du bouton de revirement horiztonal
        self.hflipPNG=PhotoImage(file=IMAGE_DIR+"horizontal-flip.png")
        #self.hflipPNG=self.hflipPNG.zoom(10)
        self.hflipPNG=self.hflipPNG.subsample(7)
        self.hflipButton = Button(self.buttonsFrame, image=self.hflipPNG,
                                     width="40", height="40",
                                     command=self.hflip)
        self.hflipButton.grid(column=6, row=0)

        # Crée le bouton de rotation
        # Ajuste la taille de l'image du bouton de rotation
        self.rotatePNG=PhotoImage(file=IMAGE_DIR+"rotate.png")
        #self.rotatePNG=self.rotatePNG.zoom(10)
        self.rotatePNG=self.rotatePNG.subsample(7)
        self.rotateButton = Button(self.buttonsFrame, image=self.rotatePNG,
                                    width="40", height="40",
            command=self.rotate)
        self.rotateButton.grid(column=7, row=0)

        # Crée le bouton de revirement vertical
        # Ajuste la taille de l'image du bouton de revirement vertical
        self.vflipPNG=PhotoImage(file=IMAGE_DIR+"vertical-flip.png")
        #self.rotatePNG=self.rotatePNG.zoom(10)
        self.vflipPNG=self.vflipPNG.subsample(7)
        self.vflipButton = Button(self.buttonsFrame, image=self.vflipPNG,
                                    width="40", height="40",
            command=self.vflip)
        self.vflipButton.grid(column=8, row=0)

        # Crée l'affichage de l'état de la capture
        self.tempsVideo = StringVar()
        self.etatCaptureLabel = Label(self.etatFrame, text=self.etatCapture[0], justify='left')
        self.etatCaptureLabel.grid(row=0,column=0, sticky='w')
        self.etatCaptureLabel2 = Label(self.etatFrame, text=self.etatCapture[1], justify='left')
        self.etatCaptureLabel2.grid(row=1,column=0, sticky='w')


        # Crée l'image "capture vidéo en cours"
        # Ajuste la taille de l'image "capture vidéo en cours"
        self.recPNG=PhotoImage(file=IMAGE_DIR+"record.png")
        #self.recPNG=self.recPNG.zoom(10)
        self.recPNG=self.recPNG.subsample(7)

        # Crée l'image "capture en cours"
        # Ajuste la taille de l'image "capture vidéo en cours"
        self.waitPNG=PhotoImage(file=IMAGE_DIR+"wait.png")
        #self.waitPNG=self.waitPNG.zoom(10)
        self.waitPNG=self.waitPNG.subsample(7)

        # Crée le menu
        self.createMenu()


    def hflip(self):

        """
	Effectue le revirement horizontal de l'image

	"""

        self.hflip = not self.hflip
        self.camera.hflip = not self.camera.hflip


    def vflip(self):

        """
	Effectue le revirement vertical de l'image

	"""

        self.vflip = not self.vflip
        self.camera.vflip = not self.camera.vflip


    def rotate(self):

        """
	Effectue la rotation de l'image

	"""

        self.angle += 90
        if self.angle == 360:
            self.angle = 0
        self.camera.rotation = self.angle


    def captureSpace(self,event):

        """
	Prends une photo avec la barre espace

	"""
        self.capture()


    def capture(self):

        """
	Prends une photo

	"""

        # Affiche une image d'attente dnas le canvas prévu à cet endroit
        imWait = self.etatCanvas.create_image((4,4), image=self.waitPNG, anchor='n'+'w')
        self.dernierFichier = self.photo_dir+self.nomFichier+"."+self.format

        # Change l'état
        self.etatCapture = ["Capture in progress...", ""]
        self.update_etatVid()

        # Prend la photo et l'enregistre sous self.dernierFichier
        self.camera.capture(self.dernierFichier)

        # Affiche l'endroit où la photo a été sauvegardée
        self.etatCapture = ["Photo saved as", self.dernierFichier]
        self.update_etatVid()

        # Efface l'image d'attente
        self.etatCanvas.delete(imWait)
        self.etatCapture = ["Ready to capture", " "]
        self.after(4000, self.update_etatVid)

        # Actualise l'aperçu de la photo prise
        self.update_capture()


    def captureSeq(self):

        """
	Prends une séquence de photos

	"""

        # Affiche une image d'attente dans le canvas prévu à cet endroit
        imWait = self.etatCanvas.create_image((4,4), image=self.waitPNG, anchor='n'+'w')
        self.etatCapture = ["Capture in sequence", "In progress..."]
        self.update_etatVid()

        # Crée la liste des fichiers dans lesquels les photos seront enregistrées
        list_seq = []
        for i in range(int(self.nbseq)):
            list_seq.append(CAPTURE_DIR+self.nomFichier+str(i)+"."+self.format)

        # Prends la séquence de photo
        self.camera.capture_sequence(list_seq,format=self.format)
        self.dernierFichier=list_seq[-1]

        # Affiche sous quels fichiers les photos ont été prises
        self.etatCapture = ["Sequence saved as", CAPTURE_DIR+self.nomFichier+"(x)."+self.format]
        self.update_etatVid()

        # Efface l'image d'attente
        self.etatCanvas.delete(imWait)
        self.etatCapture = ["Ready to capture", " "]
        self.after(4000, self.update_etatVid)
        # Actualise l'aperçu de la photo prise
        self.update_capture()


    def recVideo(self):

        """
	Prends un enregistrement vidéo
	Appelé chaque fois que le bouton vidéo est appuyé

	"""
        # Si l'enregistrement est en cours
        if self.recording:
            # Arrête l'enregistrement
            self.camera.stop_recording()

            # Efface l'image de l'enregsitrement
            self.etatCanvas.delete(self.imRec)

            # Actualise l'état
            self.etatCapture = ["Video saved as", self.fichierVid]
            self.update_etatVid()
            self.etatCapture = ["Ready to capture", ""]
            self.after(4000, self.update_etatVid)

        # Si il n'y a pas d'enregistrement en cours
        else:
            # Vérifie si la caméra est fermée
            self.camera._check_recording_stopped()

            # Affiche l'image de l'enregistrement vidéo
            self.imRec = self.etatCanvas.create_image((4,4), image=self.recPNG, anchor='n'+'w')

            # Donne le nom du fichier et commence l'enregistrement
            self.fichierVid = self.video_dir+self.nomFichier+".h264"
            self.camera.start_recording(self.fichierVid,format='h264')
            self.camera.wait_recording()

            # Actualise l'état
            self.etatCapture = ["Video recording", "In progress..."]
            self.update_etatVid()

        # Change l'état
        self.recording = not self.recording


    # Crée les liaisons entre les widgets et les événements
    def createBindings(self):

        """
	Crée les liaisons entre les widgets et les événements

	"""
        # Lorsque la fenêtre principale bouge, la position de l'aperçu en temps réel s'adaptera
        self.root.bind("<Configure>", self.set_previewPos)
        # Prends une photo en appuyant sur la barre espace
        self.root.bind("<space>", self.captureSpace)
        # Ajuste l'échelle de l'image lorsque l'utilisateur clique sur les glissoires
        self.zoomScale.bind("<B1-Motion>", self.set_previewScale)
        self.xzoomScale.bind("<B1-Motion>", self.set_previewScale)
        self.yzoomScale.bind("<B1-Motion>", self.set_previewScale)
        # Ajuste l'ISO lorsque l'utilisateur clique sur les glissoires
        self.isoScale.bind("<B1-Motion>", self.set_iso)
        # Ajuste l'ISO lorsque l'utilisateur clique sur les glissoires
        self.shutterScale.bind("<B1-Motion>", self.set_shutter)
        # Enlève la sélection de la boîte des résolutions par défaut lorsque l'utilisateur clique en dehors de celle-ci
        self.resListbox.bind('<FocusOut>', self.resListbox.selection_clear(0, "end"))


    def reset_size(self):

        """
	Effectue la réinitialisation de la taille de l'aperçu

	"""
        self.zoomScale.set(0)
        self.xzoomScale.set(50)
        self.yzoomScale.set(50)
        self.set_previewScale(None)  # event=None

        self.isoScale.set(0)
        self.shutterScale.set(0)
        self.expListbox.activate(1)
        self.set_shutter(None)  # event=None
        self.set_iso(None)  # event=None
        self.set_expmode()


    def reset_all(self):

        """
	Réinitialise tous les paramètres

	"""

        self.update_idletasks()
        self.reset_size()
        self.hflip = False
        self.camera.hflip = False
        self.vflip = False
        self.camera.vflip = False
        self.angle = 0
        self.camera.rotation = self.angle
        self.tempsButton.deselect()
        self.largeurEntry.delete(0, 'end')
        self.hauteurEntry.delete(0, 'end')
        self.textEntry.delete(0, 'end')
        self.fichierEntry.delete(0, 'end')
        self.update_nomFichier()
        self.set_overlayText()
        self.resolution = RESOLUTION_CAMERA
        self.champ = "Done"
        self.camera.resolution = self.resolution
        self.update_resactuelle()
        self.nomFichier = "capture"
        for i in range(6):
            self.formatSpinbox.invoke("buttondown")
        for i in range(10):
            self.seqSpinbox.invoke("buttondown")
        self.dernierFichier = ''
        self.update_capture()


    def quit(self):

        """
	Quitte le programme

	"""
	# Appelle le destructeur de la classe pour éviter des fuites de mémoire
        self.__del__()
        # Quitte le programme
        exit()


    """
    Cette section contient les fonctions qui fixent des variables aux attributs de la classe Application
    et qui exécute la fonction propre à cette variable

    """


    def set_previewPos(self,event):

        """
	Adjust the position of the preview to the window

	"""

        # Updates passive tasks (e.g. position of windows). Used for window geometry configuration
        self.update_idletasks()

        # Find the position of the top left corner of the preview in real time
        self.pos_preview = self.posPreview()

        # Fix the position of the preview in real time with a tuple of the form (x, y, width, height)
        self.winPreview = (self.pos_preview[0], self.pos_preview[1],
                           self.resPreview[0], self.resPreview[1])
        self.camera.preview.window = self.winPreview


    def set_overlayText(self):

        """
	Fixe le texte à afficher sur l'image

	"""
        if self.annoterTemps.get():
            # Affiche le temps sur une première ligne et le texte personnalisé sur la deuxième
            self.camera.annotate_text = "{}\n {}".format(self.temps, self.texte)

        else:
            # Affiche le texte personnalise seulement
            self.camera.annotate_text = self.texte


    def set_previewScale(self,event):

        """
	Fixe l'échelle de l'aperçu

	"""
        # Amène l'échelle du zoom en pourcentage
        # xscale et yscale correspondent à des étirements unidimensionnels en x et y respectivement,
        # d'où la multiplication par zscale pour obtenir la position
        # zscale correspond à un zoom dans l'image
        xscale, yscale, zscale = self.xzoomScale.get()/100, 1-self.yzoomScale.get()/100, self.zoomScale.get()/100

        # (x, y, w, h)
        # x,y : pourcentage de la position en x,y (gauche/haut = 0.0, droite/bas = 1.0)
        # w,h : pourcentage de la largeur/hauteur de l'image à afficher
        # avec une sécurité de 0.05 pour éviter des problèmes de mémoire
        self.camera.zoom = (xscale*zscale, yscale*zscale, 1.05-zscale, 1.05-zscale)


    def set_res(self):

        """
	Vérifie et fixe la résolution personnalisée

	"""

        # Ouvre une boîte de dialogue et soulève une exception si aucune donnée n'est entrée dans une des deux boîtes d'entrée
        if self.resPersoW.get() == '' or self.resPersoH.get() == '':
            messagebox.showinfo("Resolution Error", "Enter a whole number\nThe resolution should have the format (int, int)")
            raise ValueError("The resolution should consist of two integers")

        # Ouvre une boîte de dialogue et soulève une exception si une des données est négative
        if int(self.resPersoW.get()) < 0 or int(self.resPersoH.get()) < 0:
            messagebox.showinfo("Resolution Error", "The resolution should be a positive integer")
            raise ValueError("The resolution should be a positive integer")

        # Ouvre une boîte de dialogue et soulève une exception si une des données est inférieure à 64
        # 64x64 est la résolution minimale de la caméra
        if int(self.resPersoW.get()) < 64 or int(self.resPersoH.get()) < 64:
            messagebox.showinfo("Resolution Error", "Resolution should be greater than 64x64")
            raise ValueError("Resolution should be greater than 64x64")

        # Assigne la résolution à la caméra et soulève une exception s'il y a échec
        self.resolution = (int(self.resPersoW.get()), int(self.resPersoH.get()))

        try:
            self.camera.resolution = self.resolution
        except:
            messagebox.showinfo("Error", "The resolution is too high\nChoose a resolution lower than 2592x1944")
            raise EKameraError("The resolution is too high")

        # Ouvre une boîte de dialogue et soulève une exception si la résolution est supérieure à 2592x1944
        # 2592x1944 est la résolution maximale de la caméra sans problème de mémoire
        if self.resolution[0] > 2592 or self.resolution[1] > 1944:
            self.resolution = RESOLUTION_CAMERA
            messagebox.showinfo("Error", "The resolution is too high\nChoose a resolution lower than 2592x1944")

        # Assigne la résolution de la caméra à celle entrée par l'utilisateur
        self.camera.resolution = self.resolution
        self.camera.sensor_mode = 5
        self.champ = "Done"

        # Actualise l'aperçu de la résolution
        self.update_resactuelle()


    def set_resdef(self):

        """
	Fixe la résolution parmi les modes par défaut

	"""

        i = self.resListbox.curselection()  # Indice de l'élément sélectionné de la boîte des résolutions par défaut
        item = self.list_res[i[0]]  # Élément sélectionné de la boîte des résolutions par défaut
        self.resolution = (item[0], item[1])
        display, self.cameramode, self.champ = item[2], item[3], item[4]

        # Assigne la résolution de la caméra à celle entrée par l'utilisateur
        self.camera.resolution = self.resolution
        self.camera.sensor_mode = self.cameramode

        # Actualise l'aperçu de la résolution
        self.update_resactuelle()


    def set_sequence(self):

        """
	Fixe le nombre de photos à prendre en séquence

	"""
        self.nbseq = self.seqSpinbox.get()


    def set_iso(self,event):

        """
	Fixe l'``ISO`` de l'image

	"""
        self.camera.iso = self.isoScale.get()


    def set_shutter(self,event):

        """
	Fixe le ``shutter speed`` de l'image

	"""
        self.camera.shutter_speed = int(self.shutterScale.get())


    def set_expmode(self):

        """
	Fixe le ``mode d'exposition`` de l'image

	"""
        self.camera.exposure_mode = self.expListbox.get("active")

    """
    Cette section contient les fonctions qui actualisent les aperçus

    """

    def update_temps(self, file=True):

        """
	Actualise l'affichage du temps

	"""
        self.temps = strftime("%Y-%m-%d-%H:%M:%S" , localtime())
        self.tempsLabel.config(text=self.temps, justify='left')
        self.verify_text()
        self.after(200, self.update_temps)
        if file:
            self.update_nomFichier()


    def update_nomFichier(self):

        """
	Actualise le nom du fichier

	"""

        if self.fichierVar.get() != '':
            self.nomFichier = self.fichierVar.get() + '-' + self.temps
        else:
            self.nomFichier = 'capture' + '-' + self.temps

        self.format = self.formatSpinbox.get()

        self.apercuFichierphoto.config(text="Photo File : " + self.nomFichier + "." + self.format)
        self.apercuFichiervideo.config(text="Video File: " + self.nomFichier + ".h264")
        self.apercuRepertoirephoto.config(text="Photo Folder: " + self.photo_dir)
        self.apercuRepertoirevideo.config(text="Video Folder: " + self.video_dir)


    def update_etatVid(self):

        """
	Actualise l'état de l'enregistrement vidéo

	"""
        self.etatCaptureLabel.config(text=self.etatCapture[0])
        self.etatCaptureLabel2.config(text=self.etatCapture[1])


    def update_capture(self):

        """
	Actualise l'image de la dernière capture

	"""
        if self.dernierFichier == '':
            # Affiche l'image par défaut
            self.captureCanvas.create_image((0,0),image=self.imagedefaut, anchor='nw')
        else:
            # Affiche la dernière photo prise et adapte sa taille à la fenêtre
            self.previewCapture = PhotoImage(file=self.dernierFichier)
            scale_w = IMAGE_WIDTH/self.previewCapture.width()
            scale_h = IMAGE_HEIGHT/self.previewCapture.height()
            frac= Fraction(scale_h).limit_denominator(50)
            self.previewCapture=self.previewCapture.zoom(frac.numerator)
            self.previewCapture=self.previewCapture.subsample(frac.denominator)
            self.imCapture = self.captureCanvas.create_image((0,0),image=self.previewCapture, anchor='nw')


    def update_resactuelle(self):

        """
	Actualise l'affichage de la résolution et du champ de vision actuel

	"""
        self.resactuelleLabel.config(text="Current resolution: {}x{}".format(self.resolution[0], self.resolution[1]))
        self.champLabel.config(text="Field of view: {}".format(self.champ))


    """
    Cette section contient des fonctions de vérification et de géométrie

    """

    def verify_resW(self):

        """
	Vérifie si la résolution en largeur entrée par l'utilisateur est d'un format adéquat ``int``

	"""
        try:
            if self.resPersoW.get() == '':
                return 0
            else:
                int(self.resPersoW.get())
        except:
            # Ouvre une boîte de dialogue et soulève une exception
            messagebox.showinfo("Error", "Enter a whole number")
            raise ValueError("The resolution should consist of two integers")


    def verify_resH(self):

        """
	Vérifie si la résolution en hauteur entrée par l'utilisateur est d'un format adéquat ``int``

	"""
        try:
            if self.resPersoH.get() == '':
                return 0
            else:
                int(self.resPersoH.get())
        except:
            # Ouvre une boîte de dialogue et soulève une exception
            messagebox.showinfo("Resolution error", "Enter a whole number")
            raise ValueError("The resolution should consist of two integers")


    def verify_text(self):

        """
	Vérifie et formatte les caractères invalides du texte personnalisé

	* La fonction PiCamera.annotate_text() ne prend que les 128 premiers caractères du code ASCII

	* Remplace les caractères invalides par ``%``

	"""
        self.texte = self.textVar.get()
        for i in range(len(self.texte)):
            if ord(self.texte[i]) > 128:
                self.texte = self.texte.replace(self.texte[i], '%')
        self.set_overlayText()



    def get_cmdsize(self):

        """
        Retourne la taille des sections ``Séquence`` et ``État``

        """

        self.update_idletasks()
        w1 = self.captureFrame.winfo_reqwidth()-10
        w2 = self.commandesFrame.winfo_reqwidth()
        return (int((w1 - w2)/2), self.commandesFrame.winfo_reqheight()+7*BD)


    def posPreview(self):

        """
	Trouve la position de l'aperçu en temps réel dans l'interface

	"""
        self.update_idletasks()
        # Calculate the position of the upper left corner
        wf, hf = self.previewFrame.winfo_width(), self.previewFrame.winfo_height()
        w, h = RESOLUTION_PREVIEW
        x, y = (wf/2) - (w/2), (hf/2) - (h/2)
        pos = (int(self.sectionFrame.winfo_x() + self.imageFrame.winfo_x() +
                   self.previewFrame.winfo_x() + self.root.winfo_x() + x),
               int(self.sectionFrame.winfo_y() + self.imageFrame.winfo_y() +
                   self.previewFrame.winfo_y() + self.root.winfo_y() + y))
        return pos


    def centrerAide(self):

        """
	Place la fenêtre d'aide au centre de l'écran

	"""
        self.aide.update_idletasks()
        w = self.aide.winfo_width()
        h = self.aide.winfo_height()
        x = (self.aide.winfo_screenwidth() // 2) - (w // 2)
        y = (self.aide.winfo_screenheight() // 2) - (h // 2)
        # Ajuste l'emplacement et la taille selon les paramètres calculés
        self.aide.geometry('{}x{}+{}+{}'.format(w, h, x, y))


    def changerRepertoirePhoto(self):

        """
	Change le répertoire d'enregistrement d'un fichier photo

	* Ouvre une nouvelle fenêtre

	* self.photo_dir: str

	"""
        self.photo_dir = filedialog.askdirectory(title = "Choose a photo directory")+"/"
        self.update_nomFichier()


    def changerRepertoireVideo(self):

        """
	Change le répertoire d'enregistrement d'un fichier vidéo

	* Ouvre une nouvelle fenêtre

	* self.video_dir: str

	"""
        self.video_dir = filedialog.askdirectory(title = "Choose a video directory")+"/"
        self.update_nomFichier()
