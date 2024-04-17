SRC = """
ReCaptchaLoader.load('6LdD428fAAAAAONHdz5Ltgi-mOyfN_QUPj9JDb7O')
    .then(recaptcha => {
        return Promise.all([
            recaptcha.execute('post/create_user'),
            recaptcha.execute('post/create_user'),
            recaptcha.execute('post/create_user'),
            recaptcha.execute('post/create_user'),
            recaptcha.execute('post/create_user'),

            recaptcha.execute('post/activate_user'),
            recaptcha.execute('post/activate_user'),
            recaptcha.execute('post/activate_user'),
            recaptcha.execute('post/activate_user'),
            recaptcha.execute('post/activate_user'),
        ]).then((
            [c1,
                c2,
                c3,
                c4,
                c5,
                a1,
                a2,
                a3,
                a4,
                a5
            ]) => {
            return {
                'create': [c1, c2, c3, c4, c5],
                'activate': [a1, a2, a3, a4, a5]
            }
        })
    })
"""