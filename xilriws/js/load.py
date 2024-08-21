SRC = """
ReCaptchaLoader.load('6LdD428fAAAAAONHdz5Ltgi-mOyfN_QUPj9JDb7O')
    .then(recaptcha => {
        return Promise.all([
            recaptcha.execute('post/create_user'),
            recaptcha.execute('post/create_user'),

            recaptcha.execute('post/activate_user'),
            recaptcha.execute('post/activate_user'),
        ]).then((
            [c1,
                c2,
                a1,
                a2
            ]) => {
            return {
                'create': [c1, c2],
                'activate': [a1, a2]
            }
        })
    })
"""