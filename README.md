# Python-eksempel på innlogging med Feide

- Trykk på denne knappen: [![Run on Repl.it](https://repl.it/badge/github/jhellan/example2)](https://repl.it/github/jhellan/example2)

- Logg inn på repl.it med konto fra google, github eller facebook

- I repl.it: Gå inn i filen `main.py`. Finn linjen med `APP_BASE_URI` og bytt ut `USERNAME` med ditt brukernavn i repl.it. Brukernavnet står øverst til venstre, f.eks. `@pelle42`. Ikke ta med `@`-tegnet.

- Opprett en klient med https://dashboard.dataporten.no. Bruk knappen [ Registrer ny applikasjon ]. Sett `redirect_uri` til verdien av `APP_BASE_URI` etterfulgt av `/redirect_uri`. Godta brukervilkårene.

- Gå til 'OAuth detaljer' i dashboard og finn `client_id`. Finn linjen med `APP_CLIENT_ID` i koden og bytt ut verdien med
  din `client_id`.

- Finn `client_secret` samme sted i dashboard. Finn filen `.env` i repl.it, og bytt ut verdien bak `APP_SECRET=` med verdien av `client_secret`.

- Trykk på `Run`-knappen i repl.it

- Etter en stund dukker det opp en minibrowser i repl.it. Vi kan ikke bruke denne, men vi kan gå til samme URL i en annen tab. Logg derfra inn med Feide

- Den lokale sesjonen løper ut etter ett minutt. Det går også an å logge ut ved å gå til samme URL etterfulgt av `/logout`.

Når vi har logget inn, kommer vi til en side med info som applikasjonen har fått fra Feide:

- access\_token: En streng av hex-sifre som bare Feide kan tolke.
- id\_token: Dette er jwt med info om brukeren. I Feide inneholder den svært lite.
  Siden viser token etter dekoding.
- userinfo: Kommer fra OpenID Connect userinfo-endepunktet.
- mygroups: Gruppene innlogget bruker er med i. Kommer fra Feides gruppe-API.

Applikasjonen overlater til biblioteket `pyoidc` å håndtere innlogging. Bak kulissene gjør den 'authorization code flow'. I neste eksempel viser vi hvordan det foregår. Det vi kan se her er:

- Vi forteller biblioteket hvor det kan finne Feide, og hva det trenger å vite om applikasjonen.

- Rammeverket `flask` binder kode til URL-er i applikasjonen på denne måten:

  ```
  @app.route('/')
  def login1():
      <kode>

  @app.route('/logout')
  def logout():
      <kode>

  ```

- Autentisering osv. legges på slik: 

  ```
  @app.route('/')
  @auth.oidc_auth(AUTH_PROVIDER_NAME)
  def login1():
      <kode>

  @app.route('/logout')
  @auth.oidc_logout
  def logout():
      <kode>

  ```

- Når vi kommer til vår egen kode på hovedsiden er vi allerede innlogget. Biblioteket har lagt `access_token`, `id_token` og `userinfo` inn i brukersesjonen. Vi bruker `access_token` til å hente ut gruppeinfo. Til slutt viser vi frem alt sammen.