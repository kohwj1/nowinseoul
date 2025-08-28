function translateToast(language, text) {
    const trans_data = {
        'ko': {
                'No Search Result':'검색 결과가 없습니다',
                'Please enter a keyword':'검색어를 입력해주세요',
            },
        'ja': {
                'No Search Result':'検索結果がありません',
                'Please enter a keyword':'検索ワードを入力してください',
            },
        'en': {
                'No Search Result':'No Search Result',
                'Please enter a keyword':'Please enter a keyword',
            },
    }

    if (trans_data.hasOwnProperty(language)) {
        return trans_data[language][text];
    }
    return trans_data['en'][text];

}

function translateCrowd(language, text) {
    const trans_data = {
        'ko': {
                'Comfortable':'여유',
                'Moderate':'보통',
                'Slightly crowded':'약간 붐빔',
                'Crowded':'혼잡',
                'Go to Detail': '자세히 보기'
            },
        'ja': {
                'Comfortable':'余裕',
                'Moderate':'普通',
                'Slightly crowded':'少々混雑',
                'Crowded':'混雑',
                'Go to Detail': 'もっと見る'
            },
        'en': {
                'Comfortable':'Comfortable',
                'Moderate':'Moderate',
                'Slightly crowded':'Slightly crowded',
                'Crowded':'Crowded',
                'Go to Detail': 'Go to Detail'
            },
    }
    if (trans_data.hasOwnProperty(language)) {
        return trans_data[language][text];
    }
    return trans_data['en'][text];
}

function translateTraffic(language, text) {
    const trans_data = {
        'ko': {
                '원활':'원활',
                '서행':'서행',
                '정체':'정체'
            },
        'ja': {
                '원활':'順調',
                '서행':'混雑',
                '정체':'渋滞'
            },
        'en': {
                '원활':'Free flow',
                '서행':'Slow',
                '정체':'Congested'
            },
    }
    if (trans_data.hasOwnProperty(language)) {
        return trans_data[language][text];
    }
    return trans_data['en'][text];
}

function translateBike(language) {
    const trans_data = {
        'ko': '대',
        'ja': '台',
        'en': ' bike(s)',
    }
    if (trans_data.hasOwnProperty(language)) {
        return trans_data[language];
    }
    return trans_data['en'];
}