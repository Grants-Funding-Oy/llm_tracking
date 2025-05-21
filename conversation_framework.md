# Yrityksen LLM-näkyvyyden analyysi: Keskustelukehys

## Mitä on tehty tähän mennessä

Olemme luoneet yksinkertaisen Python-skriptin (`company_llm_analysis.py`), joka:

1. Ottaa valmiin kysymyksen suomeksi: "Miten voin hakea julkista rahoitusta yritykselleni? Kuka tarjoaa konsultointia tähän?"
2. Lähettää kysymyksen GPT-4o-mallille OpenAI:n API:n kautta
3. Tallentaa kysymyksen ja vastauksen CSV-tiedostoon myöhempää analyysia varten
4. Käyttää yksinkertaista rakennetta, jossa jokainen kysymys-vastaus-pari tallennetaan omana rivinään

## Toteutettu keskustelurakenne

Olemme nyt toteuttaneet seuraavat parannukset:

1. **Keskusteluhistorian hallinta**
   - Käytetään pandas DataFrame -rakennetta tallentamaan keskustelun tila
   - Säilytetään koko viestintähistoria OpenAI API -kutsuissa

2. **Jatkokysymys**
   - Ensimmäisen kysymyksen ("Miten voin hakea julkista rahoitusta yritykselleni? Kuka tarjoaa konsultointia tähän?") jälkeen esitetään jatkokysymys
   - Jatkokysymys: "Kerro lisää Grants-konsultointipalveluiden ominaisuuksista ja hinnoista."
   - API-kutsussa välitetään koko aiempi keskusteluhistoria kontekstin säilyttämiseksi

3. **DataFrame-pohjainen toteutus**
   - Kaikki keskustelun vaiheet tallennetaan DataFrameen, sarakkeet: 
     * ConversationID (keskustelun tunniste)
     * QuestionNumber (kysymyksen järjestysnumero keskustelussa)
     * Question (kysymyksen sisältö)
     * GPT4o_Answer (GPT-4o:n vastaus)
     * Gemini_Answer (Gemini 2.0 Flash Lite:n vastaus)
     * Timestamp (aikaleima)
     * Type (rivin tyyppi: 'question' tai 'analysis')

4. **Edut**
   - Keskustelukontekstin säilyminen tuottaa relevantimpia vastauksia
   - Aikaleiman ja keskustelutunnisteen avulla voidaan myöhemmin vertailla eri keskusteluja
   - pandas-kirjaston avulla on helppo tehdä jatkoanalyysia datasta

## LLM-vertailu

Olemme lisänneet skriptiin vertailun eri kielimallien välillä:

1. **Usean LLM-mallin käyttö**
   - Hyödynnetään sekä OpenAI:n GPT-4o-mallia että Googlen Gemini 2.0 Flash Lite -mallia
   - Samat kysymykset esitetään molemmille malleille rinnakkain
   - Mahdollistaa suoran vertailun siitä, miten eri teknologiat esittävät yritystietoja

2. **Vertaileva analyysi**
   - Analyysivaiheessa vertaillaan mallien vastauksia keskenään
   - Tunnistetaan eroja brändin esittämisessä eri mallien välillä
   - Tuottaa syvemmän ymmärryksen eri LLM-mallien käyttäytymisestä

3. **API-toteutuksien erot**
   - GPT-4o:lle välitetään keskusteluhistoria vastausten kontekstualisoimiseksi
   - Gemini-mallille lähetetään vain yksittäiset kysymykset (yksinkertaisuuden vuoksi)
   - Mahdollistaa eri API-strategioiden vertailun ja kehittämisen

## Automaattinen brändianalyysi OpenAI o3:lla

Olemme lisänneet skriptiin brändianalyysivaiheen, jossa:

1. **OpenAI o3 -mallin käyttö analyysiin**
   - Hyödynnetään OpenAI:n edistynyttä o3-mallia, joka on erikoistunut syvälliseen päättelyyn
   - O3-malli analysoi sekä GPT-4o:n että Geminin vastaukset
   - Tämä mahdollistaa erittäin laadukkaan ja syvällisen analyysin yritysnäkyvyydestä

2. **Analyysisisältö**
   - Arvioidaan miten hyvin Grants näkyy vastauksissa
   - Arvioidaan miten kielimallit esittävät Grantsin
   - Vertaillaan GPT-4o:n ja Geminin eroja yrityksen esittämisessä
   - Ehdotetaan tapoja parantaa brändin näkyvyyttä kielimallien vastauksissa
   - Tuotetaan 5 kysymystä, joilla käyttäjät todennäköisesti hakevat tietoa aiheesta

3. **Tallentaminen**
   - Analyysi tallennetaan erilliseen tekstitiedostoon (grants_analysis.txt)
   - Analyysi tallennetaan myös CSV-tiedostoon osana keskusteluhistoriaa
   - Analyysin tiivistelmä näytetään konsolissa

4. **Jatkokäyttö**
   - Analyysin tuloksia voidaan käyttää markkinointistrategian kehittämiseen
   - Tunnistetaan mahdolliset puutteet tai virheet bränditiedoissa, joita kielimallit käyttävät
   - Analyysin sisällyttäminen CSV-tiedostoon mahdollistaa sen käsittelyn osana muuta dataa

## Jatkokehityksen suunta

1. **Dynaamisten jatkokysymysten luonti**
   - Mahdollisuus luoda jatkokysymyksiä automaattisesti perustuen mallin aiempiin vastauksiin
   - Voidaan toteuttaa esim. pyytämällä mallia ehdottamaan kysymyksiä, jotka auttavat ymmärtämään paremmin yrityksen brändinäkyvyyttä

2. **Useampi keskustelu ja vertailu**
   - Mahdollisuus ajaa useita páralleeleja keskusteluja eri alkaiskysymyksillä
   - Vertailla eri yritysten näkyvyyttä samassa aihepiirissä
   - Vertailla laajempaa joukkoa kielimalleja (esim. Claude, Llama, jne.)

3. **Analyysityökalut**
   - NLP-työkalut vastausten analysointiin (esim. entiteettien tunnistaminen)
   - Visualisointi yritysten näkyvyydestä eri keskustelujen kontekstissa
   - Automaattinen raportointi LLM-mallien välisistä eroista yritysmaininnoissa

Tämä lähestymistapa mahdollistaa syvemmän analyysin siitä, miten yritykset esiintyvät LLM-vastauksissa eri keskustelukonteksteissa, eri kielimallien välillä, ja miten niiden maininnat muuttuvat keskustelun edetessä. 