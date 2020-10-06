
const baseUrl = window.location.protocol + '//' + window.location.host
const api_errors = {
    url: {
        invalid: 'Введен некоректный url.',
        required: 'Поле не должно быть пустым.',
        service_url: 'Эта ссылка уже является сокращенной.'
    },
    slug: {
        invalid: 'Короткое название может содержать только буквы, цифры, нижние подчеркивания или тире.',
        already_exists: 'Такое название уже занято.',
        max_length: 'Короткое название может содержать не более 50 символов.'
    }
}


var vm = new Vue({
    el: '#app',
    data: {
        longUrl: '',
        slug: '',
        errors: {
            url: [],
            slug: []
        },
        actionHistory: []
    },
    methods: {
        shortenUrl: async function (){
            this.resetErrors()
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    url: this.longUrl,
                    slug: this.slug
                })
            };
            const response = await fetch(baseUrl + '/shorten/', requestOptions);
            if (response.ok) {
                data = await response.json()
                urlObject = {
                    longUrl: this.longUrl,
                    shortUrl: data.url
                }
                this.addToHistory(urlObject)
                this.longUrl = data.url
                this.slug = null
            } else if (response.status == 422) {
                error = await response.json()
                this.handleError(error)
            } else {
                alert("Ошибка. Попробуйте перезагрузить страницу и выполнить запрос снова")
            };
        },
        getFieldErrors: function (fields, fieldName){
            for (error of fields[fieldName]) {
                this.errors[fieldName].push(
                    api_errors[fieldName][error.code]
                )
            }
        },
        handleError: function (error_data){
            fields = error_data.errors
            if ('url' in fields) {
                this.getFieldErrors(fields, 'url')
            }
            if ('slug' in fields) {
                this.getFieldErrors(fields, 'slug')
            }
        },
        addToHistory: function (urlObject){
            if (!this.actionHistory.some(e => e.longUrl === urlObject.longUrl &&
                                              e.shortUrl === urlObject.shortUrl)) {
                this.actionHistory.unshift(urlObject)
            }
            localStorage.setItem('history', JSON.stringify(this.actionHistory))
        },
        copyUrl: function (event, shortUrl){
            copytext = document.createElement('input')
            copytext.value = shortUrl
            document.body.appendChild(copytext)
            copytext.select()
            document.execCommand('copy')
            document.body.removeChild(copytext)

            copyButton = event.target
            copyButton.className = "btn btn-secondary"
            copyButton.innerHTML = "Скопировано"

            function changeClass() {
                copyButton.className = "btn btn-light"
                copyButton.innerHTML = "Скопировать"
            }
            setTimeout(changeClass, 1400)
        },
        resetErrors: function() {
            this.errors = {
                url: [],
                slug: []
            }
        }
    },
    beforeMount: function() {
        userHistory = localStorage.getItem('history')
        if(userHistory) {
            this.actionHistory = JSON.parse(userHistory)
        }
    }
})