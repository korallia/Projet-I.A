import array
import numpy as np

from KNN import KNN

class Image_Processor:
        def __init__(self):
            self.__nbr_metrics = 3
            self.__private = True
            

        def __inverseur(self,image):
            forme = np.where(image[:] < 1, 1, 0)
            return forme

    #fonction privé
        def __calculPerimetre(self,image):
            rslt = (np.zeros(image.shape)).astype(int)
            
            # perimetre_level2 = ((2**0.5)-1))

            #[ from-inclus : to-exclus : step ]
            gauche = image[1:-1, 0:-2]        
            droite = image[1:-1, 2:]          
            courant = image[1:-1, 1:-1]        
            haut = image[0:-2, 1:-1]        
            bas = image[2:, 1:-1]   
            # enhaut_adroite = image[0:-2,  2: ]
    

            rslt[1:-1, 1:-1] =  np.logical_or(                                                           
                    np.logical_or(np.logical_and(courant==1, gauche==0), np.logical_and(courant==1, droite==0)),      
                    np.logical_or(np.logical_and(courant==1, haut==0), np.logical_and(courant==1, bas==0))       
                    )
            
            # diagauche = np.diagonal(rslt)
            # print("---------BING BONG--------") 
            # print(rslt)   
            # x,y =np.meshgrid(np.arange(rslt.shape[1]),np.arange(rslt.shape[0]))
            # coordoner = x[:] + (rslt.shape[1]* y)
            # print(coordoner)
            # print("********")
            # coordoner_perimetre = coordoner[rslt==1]
            # print(coordoner_perimetre)
            # print(coordoner.shape)
            # droite_perimetre = coordoner_perimetre[1:-1]
            # print(droite_perimetre)
            # perimetre = np.sum( ((coordoner_perimetre + droite_perimetre)**2))**0.5
            # perimetre = (np.sum( coordoner_perimetre)**2 + np.sum(droite_perimetre) **2)**0.5

            # print(perimetre)
            
            # print(rslt)
            return rslt
            # return np.sum(rslt[rslt==1])
            
        def __calculAire(self,image):
            return np.sum(image)

        def __centroidYX(self, image):
            aire = self.__calculAire(image)
            c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
            return (np.sum(r * image), np.sum(c * image)) / aire
        
        def distance_centroide(self, image):
            centroide = self.__centroidYX(image)
            c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
            calcul = np.zeros((c[image > 0].shape[0]))
            calcul[:] = ((c[image > 0] - centroide[1]) ** 2 +
                         (r[image > 0] - centroide[0]) ** 2) ** 0.5
            return calcul

        def distance_centroide_peri(self, image):
            centroide = self.__centroidYX(image)
            data_perimetre = self.__calculPerimetre(image)
            d, s = np.meshgrid(np.arange(data_perimetre.shape[1]), np.arange(data_perimetre.shape[0]))
            calcul1 = np.zeros((d[data_perimetre > 0].shape[0]))
            calcul1[:] = ((d[data_perimetre > 0] - centroide[1]) ** 2 +
                          (s[data_perimetre > 0] - centroide[0]) ** 2) ** 0.5
            return calcul1

        def __calculComplexite(self,image):
            perimetre = self.__calculPerimetre(image)
            somme = np.sum(perimetre)
            aire = self.__calculAire(image)

            c= ((4*np.pi*aire)/somme**2)
            simpliciter = 1 - c
            return simpliciter

        def __rayon_i_sur_c(self,image):
            data_distance = self.distance_centroide(image)
            data_distance_peri = self.distance_centroide_peri(image)
            min =  np.min(data_distance_peri)
            max = np.max(data_distance)
            return   min/max

        def __aire_sur_aire_c(self,image):
            data_aire = self.__calculAire(image)
            data_distance = self.distance_centroide(image)
            max = np.max(data_distance)
            aire_circonscrit = np.pi*max**2       
            return data_aire / aire_circonscrit 

        def __singleImageProcessing(self, arrayimage):
            if ( len(arrayimage) == 2 ):
                tag = arrayimage[0]
                image  = arrayimage[1]
                forme = self.__inverseur(image)
            else:
                image = arrayimage
                forme = self.__inverseur(image)
                tag = ""
            indice1 = self.__calculComplexite(forme)
            indice2 = self.__rayon_i_sur_c(forme)
            indice3 = self.__aire_sur_aire_c(forme)


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

        @property
        def nbr_metrics(self):
            return self.__nbr_metrics
        @nbr_metrics.setter
        def nbr_metrics(self,value):
            self.__nbr_metrics = value

        
        def load_practice_images(self, images,taglist,knn):
            
            stack = np.zeros((0,2), dtype=float)
            for key, _ in enumerate(images):
                stack = np.append( stack, [(np.array([ taglist[key], images[key] ]))], axis=0)
            func = np.vectorize(self.__singleImageProcessing,  signature='(m)->(o)')
            processed = func(stack)
            
            knn.rajouter_image_a_espace_solution(processed)

        # def process_unknown_image(self, image, knn):
        #
        #     processed = self.__singleImageProcessing(image)
        #     image_processee[0, 0:3] = processed
        #     image_processee[0, 3] = knn.algo_knn(processed)
        #     return image_processee
#INTELLI_J
        def process_unknown_image(self, image,knn):
            test_image_metrics = np.zeros((4), dtype=float)#.astype(np.uint8)
            processed = self.__singleImageProcessing(image)
            tag = knn.algo_knn(processed)
            test_image_metrics[0:3] = processed
            test_image_metrics[3] = tag
            return test_image_metrics

# image_a_calculer = np.array([
       
#         [0,0,0,0,0,0,0,0,0],        # Cercle
#         [0,0,0,1,1,1,0,0,0], 
#         [0,0,1,1,1,1,1,0,0], 
#         [0,1,1,1,1,1,1,1,0], 
#         [0,1,1,1,1,1,1,1,0], 
#         [0,1,1,1,1,1,1,1,0], 
#         [0,0,1,1,1,1,1,0,0],
#         [0,0,0,1,1,1,0,0,0],
#         [0,0,0,0,0,0,0,0,0]
        
#     ])


# imgpro = Image_Processor()
# imgpro.calculPerimetre(image_a_calculer)



# image1 = np.array([
#         [0,0,0,0,0,0],          # Gros rectangle
#         [0,0,0,0,0,0], 
#         [0,1,1,1,0,0], 
#         [0,1,1,1,0,0], 
#         [0,1,1,1,0,0], 
#         [0,0,0,0,0,0],
#         [0,0,0,0,0,0]   
#     ])
# image2 = np.array([
#         [0,0,0,0,0,0],        # Petit rectangle
#         [0,0,0,0,0,0], 
#         [0,1,1,1,0,0], 
#         [0,1,1,1,0,0], 
#         [0,1,1,1,0,0], 
#         [0,1,1,1,0,0],
#         [0,0,0,0,0,0]   
#         ])

# image_list = [
# [image1],
# [image2],
# [image2]
# ]


# nom_images = {
#  0:"Gros Rectangle",
#  1:"Petit Rectangle",
#  2:"Gros H",
#  3:"Moyen H",
#  4:"Gros L",
#  5:"Étoile"
# }


# images_a_calculer = np.array(        #différentes images de départ pour tests
#     [
#       [  [0],
        
#             [np.array([
#             [0,0,0,0,0,0],          # Gros rectangle
#             [0,1,1,1,1,0], 
#             [0,1,1,1,1,0], 
#             [0,1,1,1,1,0], 
#             [0,1,1,1,1,0], 
#             [0,1,1,1,1,0],
#             [0,0,0,0,0,0]   
#         ])]
#       ]
#     ,
#      [[1],
        
#        [ np.array([
#         [0,0,0,0,0,0],        # Petit rectangle
#         [0,0,0,0,0,0], 
#         [0,1,1,1,0,0], 
#         [0,1,1,1,0,0], 
#         [0,1,1,1,0,0], 
#         [0,1,1,1,0,0],
#         [0,0,0,0,0,0]   
#         ])]]
#     ,
#      [[2],
        
#      [np.array([
#         [0,0,0,0,0,0],        # Gros H
#         [0,1,0,0,1,0], 
#         [0,1,0,0,1,0], 
#         [0,1,1,1,1,0], 
#         [0,1,0,0,1,0], 
#         [0,1,0,0,1,0],
#         [0,0,0,0,0,0]   
#     ])]],
    
#      [
#          [3],
#      [np.array([
         
#          [0,0,0,0,0,0],        # Moyen H
#          [0,1,0,1,0,0], 
#          [0,1,0,1,0,0], 
#          [0,1,1,1,0,0], 
#          [0,1,0,1,0,0], 
#          [0,1,0,1,0,0],
#          [0,0,0,0,0,0]   
#         ])]],
#      [
#          [4],
#      [np.array([
#         [0,0,0,0,0,0],        # Gros L
#         [0,1,1,0,0,0], 
#         [0,1,1,0,0,0], 
#         [0,1,1,0,0,0], 
#         [0,1,1,0,0,0], 
#         [0,1,1,1,1,1],
#         [0,1,1,1,1,1]   
#         ])]],
#      [
#          [5],
#      [np.array([
#          [0,0,0,0,0,0],        # ~Étoile
#          [0,0,0,0,0,0], 
#          [0,1,0,0,0,0], 
#          [0,0,1,1,1,1], 
#          [0,0,1,0,0,0], 
#          [0,0,0,1,1,0],
#          [0,0,0,0,0,0]   
#          ])]
#       ]
#     ])
