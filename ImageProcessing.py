import numpy as np

from KNN import KNN

class image_processe:
        def __init__(self,knn, max_distance=1, nbr_voisins=3, ):
            self.__nbr_index = 3
            self.knn = knn

    #fonction privé
        def __calculPerimetre(self,image):
            rslt = (np.zeros(image.shape)).astype(int)

    #[ from-inclus : to-exclus : step ]
            gauche = image[1:-1, 0:-2]        
            droite = image[1:-1, 2:]          
            courant = image[1:-1, 1:-1]        
            haut = image[0:-2, 1:-1]        
            bas = image[2:, 1:-1]          

            rslt[1:-1, 1:-1] =  np.logical_or(                                                           
                    np.logical_or(np.logical_and(courant==1, gauche==0), np.logical_and(courant==1, droite==0)),      
                    np.logical_or(np.logical_and(courant==1, haut==0), np.logical_and(courant==1, bas==0))       
                    )
            
            """ méthode 2 périmetre non compléter
             x,y =np.meshgrid(np.arange(rslt.shape[1]),np.arange(rslt.shape[0]))
             coordoner = x[:] + (rslt.shape[1]* y)
            print(coordoner)
            print("********")
            coordoner_perimetre = coordoner[rslt==1]
            print(coordoner_perimetre)
            divided = coordoner_perimetre[:]/coordoner.shape[1]
            modulo = coordoner_perimetre[:]%coordoner.shape[1]
            print(divided)
            print(modulo)
            print(coordoner.shape)
            droite_perimetre = coordoner_perimetre[1:-1]
            print(droite_perimetre)
            perimetre = np.sum( ((coordoner_perimetre + droite_perimetre)**2))**0.5
             perimetre = (np.sum( coordoner_perimetre)**2 + np.sum(droite_perimetre) **2)**0.5

            print(perimetre)
            """

            return np.sum(rslt[rslt==1])
            

           
        def __calculAire(self,image):
            return np.sum(image)

        def __calculComplexite(self,image):
            perimetre = self.__calculPerimetre(image)
            aire = self.__calculAire(image)

            c= (4*np.pi*aire)/perimetre**2
            simpliciter = 1 -c
            return abs(simpliciter)

        def __indice2(self,image):
            return 1
        def __indice3(self,image):
            return 0.5

        def __singleImageProcessing(self, arrayimage):
            if ( len(arrayimage) == 2 ):
                tag = arrayimage[0][0]
                image  = arrayimage[1][0]
            else:
                image = arrayimage
                tag = ""
            indice1 = self.__calculComplexite(image)
            indice2 = self.__indice2(image)
            indice3 = self.__indice3(image)


            if (tag != ""):
                return np.array([
                    indice1,
                    indice2,
                    indice3,
                    tag
                    ])
            else:
                return np.array([
                    indice1,
                    indice2,
                    indice3
                    ])



    #fonction public 
       #@property
        #def knn(self):
        #return self.__knn
        #@property
        #def nbr_metrics(self)
        #return self.__nbr_metrics


        


        
        def load_practice_images(self, images):
            func = np.vectorize(self.__singleImageProcessing,  signature='(m,n)->(o)')
            processed = func(images)
            self.knn.rajouter_image_a_espace_solution(processed)
           

        def process_unknown_image(self, image):
            processed = np.array( self.__singleImageProcessing(image))
            return self.knn.algo_knn(processed)
            





        





image_a_calculer = np.array([
        [0,0,0,0,0,0],          # Gros rectangle
        [0,0,0,0,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,0,0,0,0,0],
        [0,0,0,0,0,0]   
    ])
image1 = np.array([
        [0,0,0,0,0,0],          # Gros rectangle
        [0,0,0,0,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,0,0,0,0,0],
        [0,0,0,0,0,0]   
    ])
image2 = np.array([
        [0,0,0,0,0,0],        # Petit rectangle
        [0,0,0,0,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0],
        [0,0,0,0,0,0]   
        ])

image_list = np.array([
[image1],
[image2],
])


nom_images = {
 0:"Gros Rectangle",
 1:"Petit Rectangle",
 2:"Gros H",
 3:"Moyen H",
 4:"Gros L",
 5:"Étoile"
}


images_a_calculer = np.array(        #différentes images de départ pour tests
    [
      [  [0],
        
            [np.array([
            [0,0,0,0,0,0],          # Gros rectangle
            [0,1,1,1,1,0], 
            [0,1,1,1,1,0], 
            [0,1,1,1,1,0], 
            [0,1,1,1,1,0], 
            [0,1,1,1,1,0],
            [0,0,0,0,0,0]   
        ])]
      ]
    ,
     [[1],
        
       [ np.array([
        [0,0,0,0,0,0],        # Petit rectangle
        [0,0,0,0,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0],
        [0,0,0,0,0,0]   
        ])]]
    ,
     [[2],
        
     [np.array([
        [0,0,0,0,0,0],        # Gros H
        [0,1,0,0,1,0], 
        [0,1,0,0,1,0], 
        [0,1,1,1,1,0], 
        [0,1,0,0,1,0], 
        [0,1,0,0,1,0],
        [0,0,0,0,0,0]   
    ])]],
    
     [
         [3],
     [np.array([
         
         [0,0,0,0,0,0],        # Moyen H
         [0,1,0,1,0,0], 
         [0,1,0,1,0,0], 
         [0,1,1,1,0,0], 
         [0,1,0,1,0,0], 
         [0,1,0,1,0,0],
         [0,0,0,0,0,0]   
        ])]],
     [
         [4],
     [np.array([
        [0,0,0,0,0,0],        # Gros L
        [0,1,1,0,0,0], 
        [0,1,1,0,0,0], 
        [0,1,1,0,0,0], 
        [0,1,1,0,0,0], 
        [0,1,1,1,1,1],
        [0,1,1,1,1,1]   
        ])]],
     [
         [5],
     [np.array([
         [0,0,0,0,0,0],        # ~Étoile
         [0,0,0,0,0,0], 
         [0,1,0,0,0,0], 
         [0,0,1,1,1,1], 
         [0,0,1,0,0,0], 
         [0,0,0,1,1,0],
         [0,0,0,0,0,0]   
         ])]
      ]
    ])
      

#imgpro = image_processe()
#imgpro.load_practice_images(images_a_calculer)
#type = imgPro.process_unknown_image(image_a_calculer)
#print(nom_images[type])
#print(images_a_calculer[:,0])
array = np.zeros((2,2,1))
print("-----------")
id_list = np.array([0,1,])
array[:,0,0] = id_list[:]
array[:,1,0] = image_list
print(array)

