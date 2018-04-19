from haversine import haversine

class Get_distances:

    def __init__(self, arquivo):
        self.arquivo = arquivo

    def ler_arquivo(self):
        ref_arquivo = open(self.arquivo, "r")
        valores = [(linha[0], linha[2]) for linha in ref_arquivo]
        valores = valores[1:]
        for i in range(0, 12):
            valores[i] = [int(valores[i][0]), int(valores[i][1])]
        ref_arquivo.close()
        return valores

    def calcula_distancia(self):
        leitura = self.ler_arquivo()
        dist = [haversine(leitura[i], leitura[j]) for i in range(0, len(leitura))
                                                  for j in range(0, len(leitura))]

        return dist

if __name__ == "__main__":
    obj = Get_distances("instancias.txt")
    print(obj.calcula_distancia())
