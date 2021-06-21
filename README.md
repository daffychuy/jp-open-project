# JAP Dictionary Project

## How to run in production

```bash
go mod download
air # For development, may need to set alias "alias air='$(go env GOPATH)/bin/air'"
```

<!-- mongoimport --jsonArray --db jp --collection JMDict --file Finalize_JMdict_e.json --authenticationDatabase jp --username  --password   -->