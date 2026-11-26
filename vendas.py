from datetime import datetime
from time import sleep


def escolher_pessoa(cadastros, tipo):
    print(f"\nSelecione um {tipo}:")
    if tipo == "cliente":
        for codigo, pessoa in cadastros.items():
            print(f"CL{codigo} - {pessoa['nome']}")
    else:
        for codigo, pessoa in cadastros.items():
            print(f"VD{codigo} - {pessoa['nome']}")

    codigo_escolhido = input(f"Código do {tipo}: ").strip().upper()

    if codigo_escolhido not in cadastros:
        print(f"{tipo.capitalize()} não encontrado.")
        return None

    return codigo_escolhido

#FUNÇÃO PARA EMISSÃO DE RECIBO DE VENDAS
def emitir_recibo(venda):
    print("\n========== RECIBO DE VENDA ==========")
    print(f"Venda: n° {venda['numero']}")
    print(f"Data: {venda['data']}")
    print(f"Cliente: {venda['cliente']}")
    print(f"Vendedor: {venda['vendedor']}")
    print("--------------------")
    print(f"\n{'Produto':<18} {'Qtd.':>5} {'Unitário':>12} {'Subtotal':>12}")

    for item in venda["itens"]:
        print(f"{item['nome']:<18} {item['quantidade']:>5} R${item['valor_unitario']:>8.2f} R${item['subtotal']:>8.2f}")

    print(f"\nTOTAL DA VENDA: R$ {venda['total']:.2f}")

def realizar_venda(clientes, vendedores, produtos, vendas):
    if not clientes or not vendedores or not produtos:
        print("Cadastre pelo menos um cliente, um vendedor e um produto.")
        sleep(0.8)
        return

    codigo_cliente = escolher_pessoa(clientes, "cliente")
    if codigo_cliente is None:
        return

    codigo_vendedor = escolher_pessoa(vendedores, "vendedor")
    if codigo_vendedor is None:
        return

    carrinho = {}

    while True:
        print("\n========== PRODUTOS ==========")
        for codigo, produto in produtos.items():
            print(
                f"PR{codigo} - {produto['nome']} | "
                f"R$ {produto['valor']:.2f} | "
                f"Estoque: {produto['estoque']}"
            )

        codigo_produto = input("Código do produto (0 para finalizar, C para cancelar): ").strip().upper()

        if codigo_produto == "C":
            print("Venda cancelada.")
            return

        if codigo_produto == "0":
            break

        if codigo_produto not in produtos:
            print("Produto não encontrado.")
            sleep(0.8)
            continue

        quantidade_digitada = input("Quantidade: ").strip()

        if not quantidade_digitada.isdecimal():
            print("Digite uma quantidade inteira positiva.")
            continue

        quantidade = int(quantidade_digitada)

        if quantidade <= 0:
            print("A quantidade deve ser maior que zero.")
            continue

        quantidade_no_carrinho = 0

        if codigo_produto in carrinho:
            quantidade_no_carrinho = carrinho[codigo_produto]["quantidade"]

        estoque_disponivel = (
            produtos[codigo_produto]["estoque"] - quantidade_no_carrinho
        )

        if quantidade > estoque_disponivel:
            print(f"Estoque insuficiente. Disponível: {estoque_disponivel}.")
            sleep(0.8)
            continue

        if codigo_produto in carrinho:
            carrinho[codigo_produto]["quantidade"] += quantidade
        else:
            carrinho[codigo_produto] = {
                "codigo": codigo_produto,
                "nome": produtos[codigo_produto]["nome"],
                "quantidade": quantidade,
                "valor_unitario": produtos[codigo_produto]["valor"],
            }
        print("Adicionando produto ao carrinho", end="", flush=True)
        for ponto in range(3):
            sleep(0.5)
            print(".", end="", flush=True)
        sleep(0.5)
        print("")
    if not carrinho:
        print("Venda não realizada: carrinho vazio.")
        sleep(0.8)
        return

    itens_venda = []
    total_venda = 0

    print("\n========== CARRINHO ==========")
    for item in carrinho.values():
        item["subtotal"] = round(item["quantidade"] * item["valor_unitario"], 2)
        total_venda += item["subtotal"]
        itens_venda.append(item)
        print(f"{item['nome']} x {item['quantidade']} = R$ {item['subtotal']:.2f}")

    total_venda = round(total_venda, 2)
    print(f"Total: R$ {total_venda:.2f}")

    confirmacao = input("Confirmar venda? (s/n): ").strip().lower()

    if confirmacao not in ("s", "sim"):
        print("Venda cancelada. Estoque não alterado.")
        return

    for codigo_produto, item in carrinho.items():
        produtos[codigo_produto]["estoque"] -= item["quantidade"]

    venda = {
        "numero": len(vendas) + 1,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "vendedor": vendedores[codigo_vendedor]["nome"],
        "cliente": clientes[codigo_cliente]["nome"],
        "itens": itens_venda,
        "total": total_venda,
        "comissao": round(total_venda * 0.05, 2),
        "imposto": round(total_venda * 0.25, 2)
    }

    vendas.append(venda)

    print("\nVenda realizada com sucesso.")
    emitir_recibo(venda)

# FUNÇÃO PARA GERAR RELATÓRIOS FINANCEIROS
def gerar_relatorio(vendas):

    while True:
        while True: 
            data_inicio = input("Data inicial (DD/MM/AAAA): ")
            if not data_inicio:
                print("Você deve informar data inicial.")
                continue 
            try: 
                data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y").date()
            except ValueError:
                        print("Data inválida! Utilize o formato DD/MM/AAAA.")
                        continue
            break

        while True:
            data_fim = input("Data final (DD/MM/AAAA): ")
            if not data_fim:
                    print("Você deve informar data final.")
                    continue
            try: 
                data_fim = datetime.strptime(data_fim, "%d/%m/%Y").date()
            except ValueError:
                print("Data inválida! Utilize o formato DD/MM/AAAA.")
                continue
            if data_inicio > data_fim:
                print("A data final deve ser posterior à data inicial.")
                continue
            break
        break

    total_vendas = 0
    total_imposto = 0

    produtos_vendidos = {}
    comissao_vendedores = {}

    for venda in vendas:
        data_venda = datetime.strptime(venda["data"], "%d/%m/%Y %H:%M").date() 
        #(O .date converte venda["data"], que está exibindo a hora, para exibir apenas data)

        if data_inicio <= data_venda and data_fim >= data_venda:

            total_vendas += venda["total"]
            total_imposto += venda["imposto"]

            for item in venda["itens"]:
                nome = item["nome"]
                quantidade = item["quantidade"]

                if nome not in produtos_vendidos:
                    produtos_vendidos[nome] = 0

                produtos_vendidos[nome] += quantidade

            vendedor = venda["vendedor"]
            comissao = venda["comissao"]

            if vendedor not in comissao_vendedores:
                comissao_vendedores[vendedor] = 0

            comissao_vendedores[vendedor] += comissao

    print("\n========== RELATÓRIO FINANCEIRO ==========")
    print(f"\nPeríodo: {data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')} ")

    if total_vendas == 0:
        print("\nNenhuma venda encontrada no período informado.")
    else:
        print(f"\nTotal de vendas: R$ {total_vendas:.2f}")
        print(f"Total de impostos: R$ {total_imposto:.2f}")

    print("\n---------- PRODUTOS VENDIDOS ----------")
    if produtos_vendidos:
        for nome, quantidade in produtos_vendidos.items():
            print(f"{nome:<25} Quantidade: {quantidade}")
    else:
        print("Nenhum produto vendido no período informado.")

    print("\n---------- COMISSÕES POR VENDEDOR ----------")
    if comissao_vendedores:
        for vendedor, comissao in comissao_vendedores.items():
            print(f"{vendedor:<25} Comissão: {comissao:.2f}")
    else:
        print("Nenhuma comissão registrada no período informado.")