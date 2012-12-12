# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

class Input(OIS.KeyListener):

    velocity_x = 0;
    velocity_z = 0;
    
    # Kontruktor
    #   app     : Objekt f�r v�r huvudapplikation
    #   window  : Objekt f�r v�rat f�nster
    def __init__(self, app, window, camera):
        OIS.KeyListener.__init__(self);
        self.app = app;
        self.window = window;
        self.camera = camera;

    def __del__(self):
        self.shutdown();    

    def init(self):
        # Skapa och initialisera OIS, som �r v�rat bibliotek f�r indata fr�n
        #   saker som tagentbord och mus.
        hWnd = self.window.getCustomAttributeInt("WINDOW"); # Handle f�r v�rat f�nster
        self.inputSystem = OIS.createPythonInputSystem([("WINDOW",str(hWnd))]);
        # Skapa objekt f�r input fr�n tagentbord
        self.keyboard = self.inputSystem.createInputObjectKeyboard(OIS.OISKeyboard,True);
        # L�gg detta objekt f�r callbacks 
        self.keyboard.setEventCallback(self);

    def shutdown(self):
        # St�da upp allt vi skapat med OIS
        if(self.keyboard):
            self.inputSystem.destroyInputObjectKeyboard(self.keyboard);
        OIS.InputManager.destroyInputSystem(self.inputSystem);
        self.inputSystem = 0;

    # Denna anropas fr�n v�rat applikations-objekt en g�ng varje frame s� att vi f�r
    # en chans att g�ra saker som att l�sa indata eller flytta kameran
    #   evt     : FrameEvent, samma data som kommer i Ogre::FrameListener::frameStarted
    def frame(self, evt):
        # L�s in input-data
        if(self.keyboard):
            self.keyboard.capture();
        # Uppdatera kamerans position
        pos = self.camera.getPosition();
        # Multiplicera med timeSinceLastFrame s� vi f�r en j�mn unit/s
        pos += self.camera.getRight() * (self.velocity_x * evt.timeSinceLastFrame);
        pos += self.camera.getDirection() * (self.velocity_z * evt.timeSinceLastFrame);
        self.camera.setPosition(pos);
        # Uppdatera s� att kameran sen alltid kollar i mitten
        self.camera.lookAt(0,0,0);
    
        
    def keyPressed(self, evt):
        # Avsluta ifall escape trycks ned
        if evt.key == OIS.KC_ESCAPE:
            self.app.stop();
        if evt.key == OIS.KC_W: # Framm�t
            self.velocity_z = 150; 
        if evt.key == OIS.KC_S: # Bak�t
            self.velocity_z = -150;
        if evt.key == OIS.KC_A: # V�nster
            self.velocity_x = -250;
        if evt.key == OIS.KC_D: # H�ger
            self.velocity_x = 250;
        
        return True
 
    def keyReleased(self, evt):
        if evt.key == OIS.KC_W: # Framm�t
            self.velocity_z = 0; 
        if evt.key == OIS.KC_S: # Bak�t
            self.velocity_z = 0;
        if evt.key == OIS.KC_A: # V�nster
            self.velocity_x = 0;
        if evt.key == OIS.KC_D: # H�ger
            self.velocity_x = 0;
        return True
    
