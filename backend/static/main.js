const baseUrl = window.location.protocol + '//' + window.location.host

var vm = new Vue({
    el: '#app',
    data: {
        longUrl: null,
        slug: null,
        shortenedUrl: null,
        urlError: null,
        slugError: null,
        actionHistory: []
    },
    methods: {
        shortenUrl: async function (){
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
                alert("Ошибка. Попробуйте выполнить запрос позже")
            };
        },
        handleError: function (error){
            switch (error.error.code) {
                case "url_is_required":
                    this.urlError = "Поле не должно быть пустым."
                    break;
                case "invalid_url":
                    this.urlError = "Введен некоректный url."
                    break;
                case "invalid_slug":
                    this.slugError = "Короткое название может содержать только " +
                        "буквы, цифры нижние подчеркивания или тире и быть не больше 50 символов."
                        break;
                case "slug_already_exists":
                    this.slugError = "Такое название уже занято."
                    break;
                default:
                    break;
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
            setTimeout(this.changeClass, 1400, copyButton)
        },
        changeClass: function (elem) {
            elem.className = "btn btn-light"
            elem.innerHTML = "Скопировать"
        }
    },
    beforeMount: function() {
        userHistory = localStorage.getItem('history')
        if(userHistory) {
            this.actionHistory = JSON.parse(userHistory)
        }
    }
})