# Yrityksen LLM-näkyvyyden analyysi: Keskustelukehys

## Mitä on tehty tähän mennessä

Olemme luoneet yksinkertaisen Python-skriptin (`company_llm_analysis.py`), joka:

1. Ottaa valmiin kysymyksen suomeksi: "Miten vaihdan älylukkoon? Kuka näitä tekee?"
2. Lähettää kysymyksen GPT-4o-mallille OpenAI:n API:n kautta
3. Tallentaa kysymyksen ja vastauksen CSV-tiedostoon myöhempää analyysia varten
4. Käyttää yksinkertaista rakennetta, jossa jokainen kysymys-vastaus-pari tallennetaan omana rivinään

## Toteutettu keskustelurakenne

Olemme nyt toteuttaneet seuraavat parannukset:

1. **Keskusteluhistorian hallinta**
   - Käytetään pandas DataFrame -rakennetta tallentamaan keskustelun tila
   - Säilytetään koko viestintähistoria OpenAI API -kutsuissa

2. **Jatkokysymys**
   - Ensimmäisen kysymyksen ("Miten vaihdan älylukkoon? Kuka näitä tekee?") jälkeen esitetään jatkokysymys
   - Jatkokysymys: "Kerro lisää iLoq-älylukkojen ominaisuuksista ja hinnoista."
   - API-kutsussa välitetään koko aiempi keskusteluhistoria kontekstin säilyttämiseksi

3. **DataFrame-pohjainen toteutus**
   - Kaikki keskustelun vaiheet tallennetaan DataFrameen, sarakkeet: 
     * ConversationID (keskustelun tunniste)
     * QuestionNumber (kysymyksen järjestysnumero keskustelussa)
     * Question (kysymyksen sisältö)
     * Answer (GPT-4o:n vastaus)
     * Timestamp (aikaleima)

4. **Edut**
   - Keskustelukontekstin säilyminen tuottaa relevantimpia vastauksia
   - Aikaleiman ja keskustelutunnisteen avulla voidaan myöhemmin vertailla eri keskusteluja
   - pandas-kirjaston avulla on helppo tehdä jatkoanalyysia datasta

## Automaattinen brändianalyysi

Olemme lisänneet skriptiin brändianalyysivaiheen, joka:

1. **Analysoi iLoq-brändin näkyvyyttä LLM-vastauksissa**
   - Käyttää GPT-4o-mallia analysoimaan kerätyt vastaukset
   - Arvioi miten hyvin iLoq näkyy vastauksissa
   - Arvioi miten kielimalli esittää iLoqin

2. **Tuottaa kehitysehdotuksia**
   - Ehdottaa tapoja parantaa brändin näkyvyyttä kielimallien vastauksissa
   - Tuottaa 5 kysymystä, joilla käyttäjät todennäköisesti hakevat tietoa aiheesta

3. **Tallentaa analyysin tiedostoon**
   - Tallentaa analyysin erilliseen tekstitiedostoon (iloq_analysis.txt)
   - Näyttää analyysin tiivistelmän konsolissa

4. **Jatkokäyttö**
   - Analyysin tuloksia voidaan käyttää markkinointistrategian kehittämiseen
   - Tunnistaa mahdolliset puutteet tai virheet bränditiedoissa, joita kielimallit käyttävät

## Jatkokehityksen suunta

1. **Dynaamisten jatkokysymysten luonti**
   - Mahdollisuus luoda jatkokysymyksiä automaattisesti perustuen mallin aiempiin vastauksiin
   - Voidaan toteuttaa esim. pyytämällä mallia ehdottamaan kysymyksiä, jotka auttavat ymmärtämään paremmin yrityksen brändinäkyvyyttä

2. **Useampi keskustelu ja vertailu**
   - Mahdollisuus ajaa useita páralleeleja keskusteluja eri alkaiskysymyksillä
   - Vertailla eri yritysten näkyvyyttä samassa aihepiirissä

3. **Analyysityökalut**
   - NLP-työkalut vastausten analysointiin (esim. entiteettien tunnistaminen)
   - Visualisointi yritysten näkyvyydestä eri keskustelujen kontekstissa

Tämä lähestymistapa mahdollistaa syvemmän analyysin siitä, miten yritykset esiintyvät LLM-vastauksissa eri keskustelukonteksteissa, ja miten niiden maininnat muuttuvat keskustelun edetessä. 