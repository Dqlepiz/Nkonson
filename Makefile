
export GRANO_HOST=http://127.0.0.1:5000
export GRANO_PROJECT=Siyazana-0001
export GRANO_APIKEY=iod3omqi9avjlvx


load: loadschema loadgdocs loadjse loadpa loadwindeeds

install:
	bower install


loadschema:
	@granoloader --create-project schema data/schema.yaml

loadjse:
	@granoloader csv -t 5 data/jse/jse_entities.csv.yaml data/jse/jse_entities.csv
	@granoloader csv -t 5 data/jse/jse_links.csv.yaml data/jse/jse_links.csv

loadpa:
	./data/pa/split_pa_memberships.sh
	@granoloader csv -t 5 data/pa/pa_persons.csv.yaml data/pa/pa_persons.csv
	@granoloader csv -t 5 data/pa/pa_parties.csv.yaml data/pa/pa_parties.csv
	@granoloader csv -t 5 data/pa/pa_committees.csv.yaml data/pa/pa_committees.csv
	@granoloader csv -t 5 data/pa/pa_partymemberships.csv.yaml data/pa/pa_partymemberships.csv
	@granoloader csv -t 5 data/pa/pa_committeememberships.csv.yaml data/pa/pa_committeememberships.csv
	@granoloader csv -t 5 data/pa/pa_directorships.csv.yaml data/pa/pa_directorships.csv
	@granoloader csv -t 5 data/pa/pa_financial.csv.yaml data/pa/pa_financial.csv

loadnpo:
	@if [ ! -f data/npo/npo_organisations.csv ]; then python connectedafrica/scrapers/npo.py; fi
	@granoloader csv -t 5 data/npo/npo_organisations.csv.yaml data/npo/npo_organisations.csv
	./data/npo/matched/generate_npo_officers_matching_persons.sh
	@granoloader csv -t 5 data/npo/npo_officers.csv.yaml data/npo/matched/npo_officers.csv
	#@granoloader csv -t 5 data/npo/npo_officers.csv.yaml data/npo/npo_officers.csv  # TODO

loadwindeeds:
	./data/windeeds/split_windeeds_memberships.sh
	@granoloader csv -t 5 data/windeeds/windeeds_companies_to_members.csv.yaml data/windeeds/windeeds_companies_to_members.csv
	@granoloader csv -t 5 data/windeeds/windeeds_companies_to_directors.csv.yaml data/windeeds/windeeds_companies_to_directors.csv
	@granoloader csv -t 5 data/windeeds/windeeds_companies_to_officers.csv.yaml data/windeeds/windeeds_companies_to_officers.csv
	@granoloader csv -t 5 data/windeeds/windeeds_members_to_companies.csv.yaml data/windeeds/windeeds_members_to_companies.csv
	@granoloader csv -t 5 data/windeeds/windeeds_directors_to_companies.csv.yaml data/windeeds/windeeds_directors_to_companies.csv
	@granoloader csv -t 5 data/windeeds/windeeds_officers_to_companies.csv.yaml data/windeeds/windeeds_officers_to_companies.csv

loadwhoswho:
	@granoloader csv -t 5 data/whoswho/whoswho_persons.csv.yaml data/whoswho/whoswho_persons.csv
	#@granoloader csv -t 5 data/whoswho/whoswho_memberships.csv.yaml data/whoswho/whoswho_memberships.csv  # TODO
	@granoloader csv -t 5 data/whoswho/whoswho_qualifications.csv.yaml data/whoswho/whoswho_qualifications.csv

# Google docs
loadgdocs:
	@wget -q -O data/gdocs/persons.csv "https://docs.google.com/spreadsheets/d/1HPYBRG899R_WVW5qkvHoUwliU42Czlx8_N1l58XYc7c/export?format=csv&gid=1657155089"
	@granoloader csv -t 5 -f data/gdocs/persons.csv.yaml data/gdocs/persons.csv
	@wget -q -O data/gdocs/litigation.csv "https://docs.google.com/spreadsheets/d/1HPYBRG899R_WVW5qkvHoUwliU42Czlx8_N1l58XYc7c/export?format=csv&gid=1973809171"
	@granoloader csv -t 5 -f data/gdocs/litigation.csv.yaml data/gdocs/litigation.csv
	@wget -q -O data/gdocs/connections.csv "https://docs.google.com/spreadsheets/d/1HPYBRG899R_WVW5qkvHoUwliU42Czlx8_N1l58XYc7c/export?format=csv&gid=1752160727"
	./data/gdocs/split_connections.sh
	@granoloader csv -t 5 -f data/gdocs/personal.csv.yaml data/gdocs/personal.csv
	@granoloader csv -t 5 -f data/gdocs/family.csv.yaml data/gdocs/family.csv
	@granoloader csv -t 5 -f data/gdocs/donors.csv.yaml data/gdocs/donors.csv
	@granoloader csv -t 5 -f data/gdocs/memberships.csv.yaml data/gdocs/memberships.csv
	@granoloader csv -t 5 -f data/gdocs/partnerships.csv.yaml data/gdocs/partnerships.csv
	@granoloader csv -t 5 -f data/gdocs/financialrelations.csv.yaml data/gdocs/financialrelations.csv
	# TODO: also split up financial, affiliation, event connections

cleangdocs:
	rm data/litigation.csv data/persons.csv data/*connections.csv

# Profile images
loadprofileimages:
	@if [ ! -f data/profileimages.csv ]; then python connectedafrica/scrapers/profileimages.py; fi
	@granoloader csv -t 5 -f data/profileimages.csv.yaml data/profileimages.csv

cleanprofileimages:
	rm data/profileimages.csv
