undo_stack = []
redo_stack = []
texto_inicial = ""

def abrir_arquivo(nomearq):
    try:
        arquivo = open(nomearq, 'r', encoding='utf-8')
        texto_inicial = arquivo.read()
        arquivo.close()
        return texto_inicial
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return None

def adicionar_texto(nomearq, texto):
    try:
        arquivo = open(nomearq, 'a', encoding='utf-8')
        arquivo.write(' ' + texto)
        arquivo.close()
        undo_stack.append(('add', texto))
        redo_stack.clear()
    except FileNotFoundError:
        print("Arquivo não encontrado.")

def substituir_palavra(nomearq, palavra, sub):
    try:
        arquivo = open(nomearq, 'r', encoding='utf-8')
        texto = arquivo.read()
        arquivo.close()
        novo_texto = texto.replace(palavra, sub)
        arquivo = open(nomearq, 'w', encoding='utf-8')
        arquivo.write(novo_texto)
        arquivo.close()
        undo_stack.append(('replace', texto, novo_texto))
        redo_stack.clear()
    except FileNotFoundError:
        print("Arquivo não encontrado.")

def remover_palavra(nomearq, palavra):
    try:
        arquivo = open(nomearq, 'r', encoding='utf-8')
        texto = arquivo.read()
        arquivo.close()
        novo_texto = texto.replace(palavra, "")
        arquivo = open(nomearq, "w", encoding='utf-8')
        arquivo.write(novo_texto)
        arquivo.close()
        undo_stack.append(('remove', texto, novo_texto))
        redo_stack.clear()
    except FileNotFoundError:
        print("Arquivo não encontrado.")

def remover_texto_todo(nomearq):
    try:
        arquivo = open(nomearq, 'w', encoding='utf-8')
        arquivo.close()
        undo_stack.append(('remove_all', texto_inicial))
        redo_stack.clear()
    except FileNotFoundError:
        print("Arquivo não encontrado.")

def desfazer_acao(nomearq):
    if len(undo_stack) > 0:
        action = undo_stack.pop()
        if action[0] == 'add':
            try:
                arquivo = open(nomearq, 'r+', encoding='utf-8')
                texto = arquivo.read()
                novo_texto = texto.replace(action[1], '', 1)
                arquivo.seek(0)
                arquivo.write(novo_texto)
                arquivo.truncate()
                arquivo.close()
                redo_stack.append(('add', action[1]))
            except FileNotFoundError:
                print("Arquivo não encontrado.")
        elif action[0] == 'replace':
            try:
                arquivo = open(nomearq, 'r+', encoding='utf-8')
                texto = arquivo.read()
                novo_texto = texto.replace(action[2], action[1], 1)
                arquivo.seek(0)
                arquivo.write(novo_texto)
                arquivo.truncate()
                arquivo.close()
                redo_stack.append(('replace', action[2], action[1]))
            except FileNotFoundError:
                print("Arquivo não encontrado.")
        elif action[0] == 'remove':
            try:
                arquivo = open(nomearq, 'r+', encoding='utf-8')
                texto = arquivo.read()
                novo_texto = texto.replace(action[2], action[1], 1)
                arquivo.seek(0)
                arquivo.write(novo_texto)
                arquivo.truncate()
                arquivo.close()
                redo_stack.append(('remove', action[2], action[1]))
            except FileNotFoundError:
                print("Arquivo não encontrado.")
        elif action[0] == 'remove_all':
            try:
                arquivo = open(nomearq, 'r+', encoding='utf-8')
                arquivo.write(action[1])
                arquivo.truncate()
                arquivo.close()
                redo_stack.append(('remove_all', texto_inicial))
            except FileNotFoundError:
                print("Arquivo não encontrado.")
        else:
            print("Ação inválida")
    else:
        print("Não há ações para desfazer")

def refazer_acao(nomearq):
    if len(redo_stack) > 0:
        action = redo_stack.pop()
        if action[0] == 'add':
            try:
                arquivo = open(nomearq, 'a', encoding='utf-8')
                arquivo.write(' ' + action[1])
                arquivo.close()
                undo_stack.append(('add', action[1]))
            except FileNotFoundError:
                print("Arquivo não encontrado.")
        elif action[0] == 'replace':
            try:
                arquivo = open(nomearq, 'r+', encoding='utf-8')
                texto = arquivo.read()
                novo_texto = texto.replace(action[1], action[2], 1)
                arquivo.seek(0)
                arquivo.write(novo_texto)
                arquivo.truncate()
                arquivo.close()
                undo_stack.append(('replace', action[1], action[2]))
            except FileNotFoundError:
                print("Arquivo não encontrado.")
        elif action[0] == 'remove':
            try:
                arquivo = open(nomearq, 'r+', encoding='utf-8')
                texto = arquivo.read()
                novo_texto = texto.replace(action[1], action[2], 1)
                arquivo.seek(0)
                arquivo.write(novo_texto)
                arquivo.truncate()
                arquivo.close()
                undo_stack.append(('remove', action[1], action[2]))
            except FileNotFoundError:
                print("Arquivo não encontrado.")
        elif action[0] == 'remove_all':
            try:
                arquivo = open(nomearq, 'w', encoding='utf-8')
                arquivo.write(texto_inicial)
                arquivo.close()
                undo_stack.append(('remove_all', texto_inicial))
            except FileNotFoundError:
                print("Arquivo não encontrado.")
        else:
            print("Ação inválida")
    else:
        print("Não há ações para refazer")

while True:
    print("Seja bem-vindo(a) ao trabalho da Lilian e da Larissa")
    print("O que você deseja fazer?")
    print("1 - Abrir o arquivo")
    print("0 - Sair")
    op = int(input())

    if op == 0:
        break
    elif op == 1:
        nomearq = input("Entre com o nome do arquivo e extensão: ")
        texto_inicial = abrir_arquivo(nomearq)

        if texto_inicial is None:
            continue

        print(texto_inicial)

        while True:
            print("1 - Adicionar texto")
            print("2 - Substituir palavra no texto")
            print("3 - Remover palavra do texto")
            print("4 - Remover texto todo")
            print("5 - Desfazer")
            print("6 - Refazer")
            print("0 - Sair")
            op = int(input(">> "))

            if op == 0:
                break
            elif op == 1:
                print("Digite o texto a ser inserido:")
                texto = input(">> ")
                adicionar_texto(nomearq, texto)
            elif op == 2:
                palavra = input("Digite a palavra que deseja substituir: ")
                sub = input("Digite a nova palavra: ")
                substituir_palavra(nomearq, palavra, sub)
            elif op == 3:
                palavra = input("Digite a palavra que deseja remover: ")
                remover_palavra(nomearq, palavra)
            elif op == 4:
                remover_texto_todo(nomearq)
            elif op == 5:
                desfazer_acao(nomearq)
            elif op == 6:
                refazer_acao(nomearq)
            else:
                print("Opção inválida.")