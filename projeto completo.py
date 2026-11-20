import csv
import os
from datetime import datetime

# --- CONFIGURAÇÕES GERAIS ---
ARQUIVO = "financas.csv"
CABECALHO = ["id", "tipo", "valor", "categoria", "data", "descricao"]

# ==========================================
# FASE 1: BASE E ARQUIVOS
# ==========================================

def inicializar_arquivo():
    """Cria o arquivo com o cabeçalho se ele não existir."""
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CABECALHO, delimiter=";")
            writer.writeheader()

def adicionar_movimentacao(tipo, valor, categoria, data, descricao):
    """Adiciona uma nova receita ou despesa."""
    inicializar_arquivo()
    id_mov = datetime.now().strftime("%Y%m%d%H%M%S")
    
    with open(ARQUIVO, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CABECALHO, delimiter=";")
        writer.writerow({
            "id": id_mov,
            "tipo": tipo.lower(),
            "valor": f"{valor:.2f}",
            "categoria": categoria,
            "data": data,
            "descricao": descricao
        })
    print(f"✅ {tipo.capitalize()} de R$ {valor:.2f} registrada com sucesso!")

def listar_movimentacoes():
    """Retorna uma lista com todas as movimentações."""
    inicializar_arquivo()
    movimentacoes = []
    
    with open(ARQUIVO, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for linha in reader:
            linha["valor"] = float(linha["valor"])
            movimentacoes.append(linha)
            
    return movimentacoes


# ==========================================
# FASE 2: CÁLCULOS E RELATÓRIOS
# ==========================================

def filtrar_movimentacoes(ano, mes=None):
    """Filtra as movimentações por ano e, opcionalmente, por mês."""
    todas_movimentacoes = listar_movimentacoes()
    filtradas = []
    prefixo_data = f"{ano}-{mes:02d}" if mes else str(ano)
    
    for mov in todas_movimentacoes:
        if mov["data"].startswith(prefixo_data):
            filtradas.append(mov)
            
    return filtradas

def calcular_resumo(movimentacoes):
    """Calcula o total de receitas, despesas, saldo e gastos por categoria."""
    total_receitas = 0.0
    total_despesas = 0.0
    gastos_por_categoria = {}
    
    for mov in movimentacoes:
        valor = mov["valor"]
        
        if mov["tipo"] == "receita":
            total_receitas += valor
        elif mov["tipo"] == "despesa":
            total_despesas += valor
            categoria = mov["categoria"]
            gastos_por_categoria[categoria] = gastos_por_categoria.get(categoria, 0.0) + valor
            
    saldo = total_receitas - total_despesas
    return total_receitas, total_despesas, saldo, gastos_por_categoria

def imprimir_relatorio_mensal(ano, mes):
    """Exibe um relatório formatado para um mês específico."""
    movs_mes = filtrar_movimentacoes(ano, mes)
    
    if not movs_mes:
        print(f"\n📊 Nenhuma movimentação encontrada em {mes:02d}/{ano}.")
        return
        
    receitas, despesas, saldo, gastos_cat = calcular_resumo(movs_mes)
    
    print(f"\n{'='*30}")
    print(f"📊 RELATÓRIO MENSAL: {mes:02d}/{ano}")
    print(f"{'='*30}")
    print(f"📈 Receitas: R$ {receitas:.2f}")
    print(f"📉 Despesas: R$ {despesas:.2f}")
    print(f"💰 Saldo:    R$ {saldo:.2f}")
    print(f"\n💸 GASTOS POR CATEGORIA:")
    
    gastos_ordenados = sorted(gastos_cat.items(), key=lambda item: item[1], reverse=True)
    
    for categoria, total in gastos_ordenados:
        porcentagem = (total / despesas) * 100 if despesas > 0 else 0
        print(f"  - {categoria.ljust(15)}: R$ {total:.2f} ({porcentagem:.1f}%)")
    print(f"{'='*30}\n")


# ==========================================
# FASE 3: EDIÇÃO, REMOÇÃO E ALERTAS
# ==========================================

def salvar_todas_movimentacoes(movimentacoes):
    """Reescreve o arquivo CSV inteiro com a lista atualizada."""
    with open(ARQUIVO, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CABECALHO, delimiter=";")
        writer.writeheader()
        
        for mov in movimentacoes:
            if isinstance(mov["valor"], (float, int)):
                mov["valor"] = f"{mov['valor']:.2f}"
                
        writer.writerows(movimentacoes)

def remover_movimentacao(id_mov):
    """Remove uma movimentação buscando pelo ID."""
    movimentacoes = listar_movimentacoes()
    novas_movimentacoes = [mov for mov in movimentacoes if mov["id"] != id_mov]
    
    if len(movimentacoes) != len(novas_movimentacoes):
        salvar_todas_movimentacoes(novas_movimentacoes)
        print(f"🗑️ Movimentação {id_mov} removida com sucesso!")
        return True
        
    print(f"❌ ID {id_mov} não encontrado.")
    return False

def editar_movimentacao(id_mov, novo_valor=None, nova_categoria=None, nova_descricao=None):
    """Edita uma movimentação existente."""
    movimentacoes = listar_movimentacoes()
    editado = False
    
    for mov in movimentacoes:
        if mov["id"] == id_mov:
            if novo_valor is not None:
                mov["valor"] = novo_valor
            if nova_categoria is not None:
                mov["categoria"] = nova_categoria
            if nova_descricao is not None:
                mov["descricao"] = nova_descricao
            editado = True
            break
            
    if editado:
        salvar_todas_movimentacoes(movimentacoes)
        print(f"✏️ Movimentação {id_mov} atualizada com sucesso!")
        return True
        
    print(f"❌ ID {id_mov} não encontrado.")
    return False

def verificar_orcamento(ano, mes, limites_por_categoria):
    """Compara os gastos do mês com os limites definidos pelo usuário."""
    movs_mes = filtrar_movimentacoes(ano, mes)
    _, _, _, gastos_cat = calcular_resumo(movs_mes)
    
    print(f"\n🚨 VERIFICAÇÃO DE ORÇAMENTO: {mes:02d}/{ano} 🚨")
    print("-" * 55)
    
    for categoria, limite in limites_por_categoria.items():
        gasto = gastos_cat.get(categoria, 0.0)
        porcentagem = (gasto / limite) * 100 if limite > 0 else 0
        
        if gasto > limite:
            estouro = gasto - limite
            print(f"❌ ESTOUROU: {categoria.ljust(12)} | Limite: R$ {limite:.2f} | Gasto: R$ {gasto:.2f} (+ R$ {estouro:.2f})")
        elif porcentagem >= 80:
            print(f"⚠️ ATENÇÃO:  {categoria.ljust(12)} | Já usou {porcentagem:.1f}% de R$ {limite:.2f} (Gasto: R$ {gasto:.2f})")
        else:
            print(f"✅ OK:       {categoria.ljust(12)} | Gasto R$ {gasto:.2f} de R$ {limite:.2f}")
    print("-" * 55)


# ==========================================
# FASE 4: INTERFACE E GRÁFICOS
# ==========================================

def gerar_grafico_ascii(ano, mes):
    """Gera um gráfico de barras no terminal para as despesas do mês."""
    movs_mes = filtrar_movimentacoes(ano, mes)
    _, despesas, _, gastos_cat = calcular_resumo(movs_mes)
    
    if despesas == 0:
        print("\n📈 Sem despesas neste mês para gerar o gráfico.")
        return

    print(f"\n📊 GRÁFICO DE GASTOS ({mes:02d}/{ano}) 📊")
    print("-" * 50)
    
    gastos_ordenados = sorted(gastos_cat.items(), key=lambda x: x[1], reverse=True)
    maior_nome = max(len(cat) for cat, _ in gastos_ordenados)
    
    for categoria, valor in gastos_ordenados:
        porcentagem = valor / despesas
        tamanho_barra = int(porcentagem * 20)
        barra = "█" * tamanho_barra
        nome_alinhado = categoria.ljust(maior_nome)
        print(f"{nome_alinhado} | {barra} R$ {valor:.2f} ({(porcentagem*100):.1f}%)")
    
    print("-" * 50)

def menu_principal():
    """Loop principal que exibe o menu e gerencia as escolhas do usuário."""
    inicializar_arquivo()
    
    # Orçamento padrão de exemplo
    orcamento_mensal = {
        "Alimentação": 800.00,
        "Transporte": 300.00,
        "Lazer": 400.00,
        "Contas": 1000.00
    }
    
    while True:
        print("\n" + "="*35)
        print("💰 GERENCIADOR FINANCEIRO PESSOAL 💰")
        print("="*35)
        print("1. Adicionar Receita")
        print("2. Adicionar Despesa")
        print("3. Resumo Mensal")
        print("4. Gráfico de Gastos (ASCII)")
        print("5. Verificar Orçamento")
        print("6. Listar/Editar/Remover")
        print("0. Sair")
        print("="*35)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "0":
            print("Saindo... Cuide bem do seu dinheiro! 👋")
            break
            
        elif opcao in ("1", "2"):
            tipo = "receita" if opcao == "1" else "despesa"
            print(f"\n--- NOVA {tipo.upper()} ---")
            
            try:
                valor = float(input("Valor (R$): "))
                categoria = input("Categoria (ex: Alimentação, Salário): ").strip().title()
                data = input("Data (AAAA-MM-DD) ou enter para hoje: ").strip()
                
                if not data:
                    data = datetime.now().strftime("%Y-%m-%d")
                    
                descricao = input("Descrição rápida: ").strip()
                adicionar_movimentacao(tipo, valor, categoria, data, descricao)
            except ValueError:
                print("❌ Erro: Digite um valor numérico válido (ex: 150.50).")
                
        elif opcao == "3":
            try:
                ano = int(input("\nAno (ex: 2026): "))
                mes = int(input("Mês (1-12): "))
                imprimir_relatorio_mensal(ano, mes)
            except ValueError:
                print("❌ Erro: Digite números válidos para ano e mês.")
                
        elif opcao == "4":
            try:
                ano = int(input("\nAno (ex: 2026): "))
                mes = int(input("Mês (1-12): "))
                gerar_grafico_ascii(ano, mes)
            except ValueError:
                print("❌ Erro: Digite números válidos.")
                
        elif opcao == "5":
            try:
                ano = int(input("\nAno (ex: 2026): "))
                mes = int(input("Mês (1-12): "))
                verificar_orcamento(ano, mes, orcamento_mensal)
            except ValueError:
                print("❌ Erro: Digite números válidos.")
                
        elif opcao == "6":
            print("\n--- TODAS AS MOVIMENTAÇÕES ---")
            movs = listar_movimentacoes()
            if not movs:
                print("Nenhum registro encontrado.")
                continue
                
            for mov in movs:
                print(f"ID: {mov['id']} | {mov['data']} | {mov['tipo'].upper()} | {mov['categoria']} | R$ {mov['valor']:.2f}")
                
            acao = input("\nDeseja [E]ditar, [R]emover algum ID ou [V]oltar? ").strip().upper()
            if acao == 'R':
                id_alvo = input("Digite o ID para remover: ").strip()
                remover_movimentacao(id_alvo)
            elif acao == 'E':
                id_alvo = input("Digite o ID para editar: ").strip()
                print("Pressione ENTER sem digitar nada para manter o valor atual.")
                
                n_valor = input("Novo valor: ").strip()
                n_cat = input("Nova categoria: ").strip().title()
                n_desc = input("Nova descrição: ").strip()
                
                n_valor_float = float(n_valor) if n_valor else None
                n_cat_final = n_cat if n_cat else None
                n_desc_final = n_desc if n_desc else None
                
                editar_movimentacao(id_alvo, n_valor_float, n_cat_final, n_desc_final)
                
        else:
            print("❌ Opção inválida. Tente novamente.")

# Executa o programa
if __name__ == "__main__":
    menu_principal()