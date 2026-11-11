vendedores = {
    1 : "Carlos",
    2 : "Maria"}

clientes = {}
nome = ""
id_cliente = 1;

produtos = {
    1 : ["bolacha", 5.00, 10],
    2 : ["carne", 10.00, 20]} 
print(produtos[1][1])

while True:
    confirm = input("Adicionar cliente? (s/n)").lower
    nome = input("Nome do cliente: ").capitalize()
    if nome == "Sair":
        print("Encerrando...")
        break
    while True:
        if confirm == "s":
            clientes[id] = nome

