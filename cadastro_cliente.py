from datetime import datetime
import msvcrt

def data_de_nascimento():
    numeros = ""
    mensagem = "Informe a data de nascimento (DD/MM/AAAA): "

    print(mensagem, end="", flush=True)

    while len(numeros) < 8:
        tecla = msvcrt.getwch()
        if tecla.isdigit():
            numeros += tecla
        elif tecla == "\b" and numeros:
            numeros = numeros[:-1]
        if len(numeros) <= 2:
            data = numeros
        elif len(numeros) <= 4:
            data = numeros[:2] + "/" + numeros[2:]
        else:
            data = numeros[:2] + "/" + numeros[2:4] + "/" + numeros[4:]

        print("\r\x1b[2K" + mensagem + data, end="", flush=True)

    print()
    return data

def cadastro_cliente(cliente):
      id = 1
      while f"{id:04d}" in cliente:
            id += 1
      
      while True:
            cadastro = input("Deseja Cadastrar o cliente? (s/n) ").strip().lower()
            if cadastro.strip().lower() in ("sim", "s"):

                  while True:
                        nome = input("Informe o nome do cliente: ").title().strip()
                        if not " " in nome:
                              print("Você deve fornecer nome e sobrenome para prosseguir")
                              continue
                        elif len(nome) > 30:
                              print("nome invalido por execesso de caracteres, por favor informe apenas nome e sobrenome")
                              continue
                        data_nascimento = data_de_nascimento()
                        try:
                          nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
                        except ValueError:
                          print("Data inválida!")
                          continue
                        hoje = datetime.today()
                        idade = hoje.year - nascimento.year
                        if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
                         idade -= 1
                        endereco = input("Informe o endereço do cliente: ").strip().title()
                        cpf = input("Informe o CPF do cliente sem traços ou pontos : ")
                        cpf = cpf.replace(".", "").replace("-", "")
                        if len(cpf) != 11 or not cpf.isdigit():
                              print("CPF inválido!")
                              continue
                        cliente[f"{id:04d}"] = {"nome": nome, "data de nascimento": data_nascimento, "CPF": cpf, "Endereço": endereco, "idade": idade }
                        id += 1

                        while True:
                              add = input("Deseja cadastrar mais clientes? (s/n) ").strip().lower()
                              if add.strip().lower() in ("sim", "s", "não", "nao", "n"):
                                    break
                              print("Não entendi, poderia informar novamente ? ")
                        if add.strip().lower() in ("não", "nao", "n"):
                              print("Saindo...")
                              break
                  break 
            elif cadastro.strip().lower() in ("não", "nao", "n"):
                  print("Saindo...")
                  break
            else:
                  print("Não entendi, poderia me informar novamente ? ")
      return cliente

      
def mostrar_cliente(cliente):
      print("=" * 20)
      for id, dados in cliente.items():
            print(f"nome: {dados['nome']}")
            print(f"data de nascimento: {dados['data de nascimento']}")
            print(f"idade:{dados['idade']}")
            print(f"CPF: {dados['CPF'][:3]}.{dados['CPF'][3:6]}.{dados['CPF'][6:9]}-{dados['CPF'][9:]}")
            print(f"Endereço: {dados['Endereço']}")
            print(f"ID: CL{id}")
            print("=" * 20)
if __name__ == "__main__":
      cliente = {}
      cadastro_cliente(cliente)
      mostrar_cliente(cliente)
