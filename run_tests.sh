rm -rf allure-results allure-report
rm -rf screenshots/*
rm -rf fail_case_screenshot
pytest
allure generate allure-results --clean -o allure-report
echo Allure HTML report generated at: allure-report/index.html
