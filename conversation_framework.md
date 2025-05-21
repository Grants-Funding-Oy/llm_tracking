# Yrityksen LLM-näkyvyyden analyysi: Keskustelukehys

## Mitä on tehty tähän mennessä

Olemme luoneet yksinkertaisen Python-skriptin (`company_llm_analysis.py`), joka:

1. Ottaa valmiin kysymyksen suomeksi: "Miten vaihdan älylukkoon? Kuka näitä tekee?"
2. Lähettää kysymyksen GPT-4o-mallille OpenAI:n API:n kautta
3. Tallentaa kysymyksen ja vastauksen CSV-tiedostoon myöhempää analyysia varten
4. Käyttää yksinkertaista rakennetta, jossa jokainen kysymys-vastaus-pari tallennetaan omana rivinään

## Jatkokehityksen suunta: Keskustelurakenne

Seuraava kehitysvaihe on rakentaa aito keskustelukokemus, jossa:

1. **Keskusteluhistorian hallinta**
   - Käytetään pandas DataFrame -rakennetta tallentamaan keskustelun tila
   - Säilytetään koko viestintähistoria OpenAI API -kutsuissa

2. **Jatkokysymysten lisääminen**
   - Ensimmäisen vastauksen jälkeen esitetään jatkokysymyksiä
   - Jatkokysymykset voivat olla joko:
     * Etukäteen määriteltyjä kysymyksiä, jotka syventävät keskustelua
     * Dynaamisesti luotuja kysymyksiä perustuen aiempiin vastauksiin

3. **DataFrame-pohjainen toteutus**
   - Kaikki keskustelun vaiheet tallennetaan DataFrameen, esim. sarakkeet: 
     * QuestionsID (keskustelun tunniste)
     * QuestionNumber (kysymyksen järjestysnumero keskustelussa)
     * Question (kysymyksen sisältö)
     * Answer (GPT-4o:n vastaus)
     * Timestamp (aikaleima)

4. **Edut**
   - Mahdollistaa monimutkaisempien keskustelujen mallintamisen
   - Helpottaa tiedon jatkokäsittelyä pandas-työkaluilla
   - Parantaa yritysmainintojen kontekstuaalista analyysia
   - Mahdollistaa erilaisten keskustelupolkujen vertailun

## Käytännön toteutus jatkossa

1. Päivitetään skripti käyttämään pandas-kirjastoa
2. Lisätään logiikka, joka tallentaa keskustelun tilan DataFrameen
3. Määritellään jatkokysymysten logiikka (esim. "Mitä älylukon vaihtaminen maksaa?" tai "Kertoisitko lisää iLoq-lukkojen ominaisuuksista?")
4. Parannetaan CSV-tallennusta sisältämään koko keskusteluhistoria

Tämä lähestymistapa mahdollistaa syvemmän analyysin siitä, miten yritykset esiintyvät LLM-vastauksissa eri keskustelukonteksteissa, ja miten niiden maininnat muuttuvat keskustelun edetessä. 