import numpy as np

class KNN:
    def __init__(self,nbr_elements,nbr_metric=3, nbr_voisins =3):
        self.__nbr_voisins = nbr_voisins
        self.__nbr_metrics = nbr_metric
        self.__nbr_elements = nbr_elements
        self.__espace_solution = np.zeros((self.__nbr_elements,self.__nbr_metrics+1))
        self.__private = True
        self.__tab_distance = np.empty((self.__nbr_elements, 2))
#private function

    def __resize(self):
        del(self.__espace_solution)
        self.__espace_solution = np.zeros((self.__nbr_elements,self.__nbr_metrics+1))

    def __clear(self):
        self.espace_solution[:] =0

    def __calcule_distance(self,point_comparaison):
        self.__tab_distance[:, 0] =  np.sum( ((self.__espace_solution[:, 0:self.__nbr_metrics] -point)**2),axis=1)**0.5
        self.__tab_distance[:, -1] =  self.__espace_solution[:, -1]

        tab_indices =self.__tab_distance[:, 0].argsort()
        tab_indices_trier = tab_indices[:self.nbr_voisins]
        return self.__tab_distance[tab_indices_trier]


    def __determiner_type(resultat):
        pass
    #####continuer######
        
        
       

        
                #public functions
    @property
    def nbr_voisins(self):
        return self.__nbr_voisins

    @nbr_voisins.setter
    def nbr_voisins(self,value):
        self.nbr_voisins = value
        
    @property
    def nbr_metrics(self):
        return self.__nbr_metrics


    @nbr_metrics.setter
    def nbr_metrics(self,value):
        self.__nbr_metrics = value
        self.__resize()
        
    @property
    def nbr_elements(self):
        return self.__nbr_elements

    @nbr_elements.setter
    def nbr_elements(self,value):
        self.__nbr_elements = value
        self.__resize()    

    @property
    def espace_solution(self):
        return self.__espace_solution


    def rajouter_image_a_espace_solution(self,images_a_ajouter):
        self.__espace_solution = images_a_ajouter


    def algo_knn(self,point_comparaison):
        resultat =self.__calcule_distance(point_comparaison)

       
       

   
        
knn = KNN(5)
images_a_ajouter = np.array(
    [
        [1,2,1,1],
        [1,4,1,1],
        [1,1,7,2],
        [1,3,1,3],
        [1,1,8,1]
        ]
        )
knn.rajouter_image_a_espace_solution(images_a_ajouter)
point = np.array([1,4,6])
knn.calcule_distance(point)        


        


        


