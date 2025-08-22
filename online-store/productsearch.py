import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import date

# -----------------------------
# Apufunktiot
# -----------------------------


def get_float_input(prompt):
    """Pyytää käyttäjältä luvun, muuntaa pilkut pisteiksi."""
    while True:
        val = input(prompt).strip().replace(",", ".")
        try:
            return float(val)
        except ValueError:
            print("⚠️ Anna kelvollinen numero.")


def break_even_roas(cost, price):
    """Laskee BE ROAS (break-even ROAS)."""
    if price <= cost:
        return None
    return price / (price - cost)


def interpret_be_roas(be_roas):
    """Tulkitsee BE ROAS -arvon kannattavuuden mukaan."""
    if be_roas is None:
        return "Ei katetta"
    elif be_roas < 2:
        return "Hyvä kannattavuus (helppo saada voittoa)"
    elif be_roas <= 3.5:
        return "Kohtalainen (riippuu markkinasta ja kilpailusta)"
    elif be_roas > 4:
        return "Heikko kannattavuus (vaikea saada voittoa)"
    return "Tuntematon"


def scrape_reviews_aliexpress(url):
    """Yrittää hakea arvostelut Aliexpressistä."""
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(" ", strip=True)
        match = re.search(r"(\d+(\.\d+)?)[ ]*/[ ]*5", text)
        if match:
            return match.group(0)
    except:
        pass
    return None


def scrape_reviews_amazon(url):
    """Yrittää hakea arvostelut Amazonista."""
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        review_element = soup.find("span", {"id": "acrCustomerReviewText"})
        if review_element:
            return review_element.get_text(strip=True)
        rating_element = soup.find("span", {"class": "a-icon-alt"})
        if rating_element:
            return rating_element.get_text(strip=True)
    except:
        pass
    return None


def parse_reviews(text):
    """Normalisoi arvostelutekstin → esim. 4.6/5 (1200 arvostelua)."""
    if not text:
        return "Ei tietoa"
    rating = re.search(r"(\d+(\.\d+)?)[ ]*/[ ]*5", text)
    count = re.search(r"(\d{2,})", text.replace(",", ""))
    rating_val = rating.group(0) if rating else ""
    count_val = count.group(0) if count else ""
    if rating_val and count_val:
        return f"{rating_val} ({count_val} arvostelua)"
    elif rating_val:
        return rating_val
    elif count_val:
        return f"{count_val} arvostelua"
    return text


# -----------------------------
# Pääfunktio
# -----------------------------

def save_product():
    today = date.today().strftime("%d.%m.%Y")

    ad_link = input("Anna mainoslinkki: ")
    product_name = input("Anna tuotteen nimi: ")
    competitor_store = input("Anna kilpailijan kauppa: ")
    aliexpress_link = input("Anna Aliexpress-linkki: ")
    amazon_link = input("Anna Amazon-linkki: ")

    # Arvostelut automaattisesti tai käyttäjältä
    aliexpress_reviews = scrape_reviews_aliexpress(aliexpress_link)
    if not aliexpress_reviews:
        aliexpress_reviews = input(
            "❓ Anna Aliexpress-arvostelut (esim. 4.6/5, 1200 arvostelua): ")
    aliexpress_reviews = parse_reviews(aliexpress_reviews)

    amazon_reviews = scrape_reviews_amazon(amazon_link)
    if not amazon_reviews:
        amazon_reviews = input(
            "❓ Anna Amazon-arvostelut (esim. 4.4/5, 5000 arvostelua): ")
    amazon_reviews = parse_reviews(amazon_reviews)

    # Hinnat
    cost_price = get_float_input("Anna ostohinta (€): ")
    selling_price = get_float_input("Anna myyntihinta (€): ")

    profit = selling_price - cost_price
    be_roas = break_even_roas(cost_price, selling_price)
    be_roas_str = f"{be_roas:.2f}" if be_roas else "Ei katetta"
    be_roas_eval = interpret_be_roas(be_roas)
    analysis = "Voitollista" if profit > 0 else "Nollatulos" if profit == 0 else "Tappiollista"

    # Lisäkysymykset
    q_interest = input("Herättääkö kiinnostusta? (k/e): ")
    q_problem = input("Ratkaiseeko ongelman? (k/e): ")
    q_clear = input("Helppo ymmärtää? (k/e): ")
    q_social = input("Kiinnostava somessa? (k/e): ")
    q_marketing = input("Useita markkinointikulmia? (k/e): ")
    q_trend = input("Mainosmäärät kasvavia vai laskevia? (k/e): ")

    # Tallennus projektikansioon
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, "Jounin-tuotekandit.txt")

    content = f"""
Päivämäärä: {today}
Tuote: {product_name}
Kilpailijan kauppa: {competitor_store}
Mainoslinkki: {ad_link}
Aliexpress-linkki: {aliexpress_link}
Arvostelut Aliexpress: {aliexpress_reviews}
Amazon-linkki: {amazon_link}
Arvostelut Amazon: {amazon_reviews}
Ostohinta (€): {cost_price:.2f}
Myyntihinta (€): {selling_price:.2f}
Voitto (€): {profit:.2f}
BE ROAS: {be_roas_str} ({be_roas_eval})
Analyysi: {analysis}
Herättääkö kiinnostusta?: {q_interest}
Ratkaiseeko ongelman?: {q_problem}
Helppo ymmärtää?: {q_clear}
Kiinnostava somessa?: {q_social}
Useita markkinointikulmia?: {q_marketing}
Trendikäs (FB Ads): {q_trend}
---------------------------------------------------------
"""

    with open(filename, "a", encoding="utf-8") as f:
        f.write(content)

    print(f"\n✅ Tiedot tallennettu tiedostoon: {filename}")


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    while True:
        save_product()
        again = input("\n➕ Lisätäänkö toinen tuote? (k/e): ").strip().lower()
        if again != "k":
            print("👋 Ohjelma lopetettu. Kiitos!")
            break
