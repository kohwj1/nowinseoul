const langSelectBox = document.getElementById('lang-select');
const url = new URL(window.location.href);
const pathName = url.pathname;
const pathSegments = pathName.split('/');

function userLocale() {
    // const url = new URL(window.location.href);
    // const pathName = url.pathname;
    // const pathSegments = pathName.split('/');
    // console.log(pathSegments)

    if (pathSegments.length === 0) {
        return 'en'
    }
    return pathSegments[1];
}

document.addEventListener('DOMContentLoaded', () => {
    const locale = userLocale()
    console.log(locale)
    document.getElementById(locale).setAttribute('selected','');
})

langSelectBox.addEventListener('change', () => {
    const newLang = langSelectBox.value;
    console.log(newLang)
    const currentLocation = pathSegments[2]

    switch(currentLocation) {
        case "":
            location.href = `/${newLang}`
            break;
        case "map":
            location.href = `/${newLang}/map`
            break;
        case "detail":
            location.href = `/${newLang}/detail/${pathSegments[3]}`
            break;
    }
})