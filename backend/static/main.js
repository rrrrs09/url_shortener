const baseUrl = window.location.protocol + '//' + window.location.host

var vm = new Vue({
    el: '#app',
    data: {
        longUrl: null,
        slug: null,
        shortenedUrl: null,
        urlError: null,
        slugError: null
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
                this.longUrl = data.data.url
                this.slug = null
            } else if (response.status == 422) {
                error = await response.json()
                this.handleError(error)
            } else {
                alert("Ошибка. Попробуйте выполнить запрос позже")
            };
        },
        handleError: function (error){
            console.log(error.error.code)
            switch (error.error.code) {
                case "urlIsRequired":
                    this.urlError = "Поле не должно быть пустым."
                    break;
                case "invalidUrl":
                    this.urlError = "Введен некоректный url."
                    break;
                case "slugValidation":
                    this.slugError = "Короткое название может содержать только буквы, цифры и тире."
                        break;
                case "slugAlreadyExists":
                    this.slugError = "Такое название уже занято."
                    break;
                default:
                    break;
            }
        }
    }
})