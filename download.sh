base_url="https://res.data.gov.hk/api/get-download-file?name=https%3A%2F%2Fresource.data.one.gov.hk%2Fdoj%2Fdata%2F"

mkdir -p raw_legislation
cd raw_legislation
languages=(en)

for lang in ${languages[@]}; do
    echo "Downloading ${lang}"
    wget -O cap_1_cap_300_${lang}.zip ${base_url}hkel_c_leg_cap_1_cap_300_${lang}.zip
    wget -O cap_301_cap_600_${lang}.zip ${base_url}hkel_c_leg_cap_301_cap_600_${lang}.zip
    wget -O cap_601_cap_end_${lang}.zip ${base_url}hkel_c_leg_cap_601_cap_end_${lang}.zip
    unzip cap_1_cap_300_${lang}.zip -d ${lang}
    unzip cap_301_cap_600_${lang}.zip -d ${lang}
    unzip cap_601_cap_end_${lang}.zip -d ${lang}
done
