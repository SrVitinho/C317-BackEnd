import os
import requests
from keys import link
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
IMAGENS_DIR = BASE_DIR.parent / "imagenspop"
BASE_URL = link + "item/create/"

itens = [
    {"Nome": "Cosmopolitan", "Descricao": "Drink clássico com vodka, licor de laranja, limão e cranberry.",
     "Categoria": "alcoolicos", "Preco": 25.0, "Ativo": True, "Imagem": "cosmopolitan.jpg"},
    {"Nome": "Mojito", "Descricao": "Rum, hortelã, açúcar, limão e água com gás.", "Categoria": "alcoolicos",
     "Preco": 22.0, "Ativo": True, "Imagem": "mojito.jpg"},
    {"Nome": "Bellini", "Descricao": "Prosecco e purê de pêssego.", "Categoria": "alcoolicos", "Preco": 20.0,
     "Ativo": True, "Imagem": "bellini.jpg"},
    {"Nome": "Dry Martini", "Descricao": "Gin e vermute seco.", "Categoria": "alcoolicos", "Preco": 23.0, "Ativo": True,
     "Imagem": "dry_martini.jpg"},
    {"Nome": "Blood Mary", "Descricao": "Vodka, suco de tomate, especiarias.", "Categoria": "alcoolicos", "Preco": 24.0,
     "Ativo": True, "Imagem": "blood_mary.jpg"},
    {"Nome": "Pina Colada", "Descricao": "Rum, leite de coco, suco de abacaxi.", "Categoria": "alcoolicos",
     "Preco": 26.0, "Ativo": True, "Imagem": "pina_colada.jpg"},
    {"Nome": "Margarita Tradicional", "Descricao": "Tequila, Cointreau e limão.", "Categoria": "alcoolicos",
     "Preco": 28.0, "Ativo": True, "Imagem": "margarita_tradicional.jpg"},
    {"Nome": "Negroni", "Descricao": "Gin, Campari e vermute rosso.", "Categoria": "alcoolicos", "Preco": 27.0,
     "Ativo": True, "Imagem": "negroni.jpg"},
    {"Nome": "Clericot", "Descricao": "Vinho branco, frutas e gelo.", "Categoria": "alcoolicos", "Preco": 21.0,
     "Ativo": True, "Imagem": "clericot.jpg"},
    {"Nome": "Old Fashioned", "Descricao": "Whisky, açúcar e Angostura.", "Categoria": "alcoolicos", "Preco": 29.0,
     "Ativo": True, "Imagem": "old_fashioned.jpg"},
    {"Nome": "Whisky Sour", "Descricao": "Whisky, suco de limão e açúcar.", "Categoria": "alcoolicos", "Preco": 28.0,
     "Ativo": True, "Imagem": "whisky_sour.jpg"},
    {"Nome": "Tom Collins", "Descricao": "Gin, suco de limão, açúcar e água com gás.", "Categoria": "alcoolicos",
     "Preco": 23.0, "Ativo": True, "Imagem": "tom_collins.jpg"},
    {"Nome": "Sex on the Beach", "Descricao": "Vodka, licor de pêssego, suco de laranja e cranberry.",
     "Categoria": "alcoolicos", "Preco": 24.0, "Ativo": True, "Imagem": "sex_on_the_beach.jpg"},
    {"Nome": "Moscow Mule", "Descricao": "Vodka, limão e espuma de gengibre.", "Categoria": "alcoolicos", "Preco": 26.0,
     "Ativo": True, "Imagem": "moscow_mule.jpg"},
    {"Nome": "Gin Tônica", "Descricao": "Gin e água tônica.", "Categoria": "alcoolicos", "Preco": 22.0, "Ativo": True,
     "Imagem": "gin_tonica.jpg"},
    {"Nome": "Caipirinhas", "Descricao": "Cachaça, limão e açúcar.", "Categoria": "alcoolicos", "Preco": 20.0,
     "Ativo": True, "Imagem": "caipirinha.jpg"},
    {"Nome": "Cirque Blue", "Descricao": "Drink azul tropical.", "Categoria": "alcoolicos", "Preco": 24.0,
     "Ativo": True, "Imagem": "cirque_blue.jpeg"},
    {"Nome": "Pink Lemonade", "Descricao": "Limonada cor-de-rosa.", "Categoria": "nao_alcoolicos", "Preco": 18.0,
     "Ativo": True, "Imagem": "pink_lemonade.jpg"},
    {"Nome": "Pina Descolada", "Descricao": "Versão divertida da pina colada.", "Categoria": "alcoolicos",
     "Preco": 26.0, "Ativo": True, "Imagem": "pina_descolada.jpg"},
    {"Nome": "Lichia Paradise", "Descricao": "Drink exótico de lichia.", "Categoria": "alcoolicos", "Preco": 27.0,
     "Ativo": True, "Imagem": "lichia_paradise.jpg"},
    {"Nome": "Sonho Brilhante", "Descricao": "Drink surpresa com glitter.", "Categoria": "alcoolicos", "Preco": 28.0,
     "Ativo": True, "Imagem": "sonho_brilhante.jpg"},

    {"Nome": "Cerveja Stella Artois", "Descricao": "Cerveja Stella Artois 250ml.", "Categoria": "outras_bebidas",
     "Preco": 12.0, "Ativo": True, "Imagem": "stella.jpg"},
    {"Nome": "Whisky Black Label", "Descricao": "Whisky Johnnie Walker Black Label.", "Categoria": "outras_bebidas",
     "Preco": 45.0, "Ativo": True, "Imagem": "black_label.jpg"},
    {"Nome": "Whisky Johnnie Walker Red Label", "Descricao": "Whisky Johnnie Walker Red Label.",
     "Categoria": "outras_bebidas", "Preco": 40.0, "Ativo": True, "Imagem": "red_label.jpg"},
    {"Nome": "Espumante Freixe Brut", "Descricao": "Espumante Freixe Brut.", "Categoria": "outras_bebidas",
     "Preco": 60.0, "Ativo": True, "Imagem": "freixe_brut.png"},
    {"Nome": "Espumante Salton Brut", "Descricao": "Espumante Salton Brut.", "Categoria": "outras_bebidas",
     "Preco": 55.0, "Ativo": True, "Imagem": "salton_brut.jpg"},

    {"Nome": "Drink na Lâmpada", "Descricao": "Drink estiloso servido em lâmpada.", "Categoria": "shots", "Preco": 30.0,
     "Ativo": True, "Imagem": "drink_lampada.jpg"},

    {"Nome": "Estrutura de Bar Personalizada", "Descricao": "Consultar modelos.",
     "Categoria": "estrutura", "Preco": 1000.0, "Ativo": True, "Imagem": "bar.jpg"},

    {"Nome": "Bartender", "Descricao": "Profissional responsável pela preparação dos drinks.",
     "Categoria": "funcionarios", "Preco": 150.0, "Ativo": True, "Imagem": "bartender.jpg"},
    {"Nome": "Garçon", "Descricao": "Profissional responsável pela entrega de comidas e bebidas.",
     "Categoria": "funcionarios", "Preco": 100.0, "Ativo": True, "Imagem": "garcon.png"},
]

for item in itens:
    imagem_path = IMAGENS_DIR / item['Imagem']
    with open(imagem_path, "rb") as img_file:
        response = requests.post(
            BASE_URL,
            files={"image": img_file},
            data={
                "Nome": item['Nome'],
                "Descricao": item['Descricao'],
                "Categoria": item['Categoria'],
                "Preco": item['Preco'],
                "Ativo": str(item['Ativo']).lower()
            }
        )
    print(f"Item {item['Nome']} - Status: {response.status_code} - {response.text}")
