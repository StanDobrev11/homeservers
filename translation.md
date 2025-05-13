## Updating Translations in the Future
If you make changes to your templates or add new strings:
1. Re-extract the messages:
``` bash
   pybabel extract -F babel.cfg -o messages.pot .
```
1. Update the translation files:
``` bash
   pybabel update -i messages.pot -d translations
```
1. Edit the updated messages.po files
2. Compile the translations:
``` bash
   pybabel compile -d translations
```
This implementation should give you a fully translatable Flask application that can switch between English and Bulgarian. Users can choose their preferred language, and all content including emails will be in the selected language.
