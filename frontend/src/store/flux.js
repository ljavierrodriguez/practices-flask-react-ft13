const getState = ({ getStore, getActions, setStore }) => {
    return {
        store: {
            urlAPI: "https://5000-beige-mollusk-2as0uldj.ws-us20.gitpod.io",
            currentUser: null,
            error: null,
            email: '',
            password: '',
            users: null,
        },
        actions: {
            getCurrentUser: () => {
                if (sessionStorage.getItem('currentUser')) {
                    const currentUser = JSON.parse(sessionStorage.getItem('currentUser'));
                    let date = new Date();
                    console.log(date)
                    if (date.getUTCDate() > currentUser.expire_date) {
                        sessionStorage.clear();
                        setStore({
                            currentUser: null
                        })
                    } else {
                        setStore({
                            currentUser: currentUser
                        })
                    }
                }
            },
            getLogin: (email, password) => {
                const { urlAPI } = getStore();
                fetch(`${urlAPI}/api/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email,
                        password
                    })
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.email || data.password || data.faild) {
                            setStore({
                                error: data
                            })
                        } else {
                            setStore({
                                error: null,
                                email: '',
                                password: '',
                                currentUser: data
                            })
                            sessionStorage.setItem('currentUser', JSON.stringify(data));
                        }
                    })
            },
            loginSubmit: (e) => {
                e.preventDefault();
                const { getLogin } = getActions();
                const { email, password } = e.target;
                console.log(email, password);
                getLogin(email.value, password.value);
            },
            loginChange: (e) => {
                const { name, value } = e.target;
                setStore({
                    [name]: value
                })
            },
            getUsers: (token) => {
                const { urlAPI } = getStore();
                fetch(`${urlAPI}/api/users`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token,
                    }
                })
                    .then(resp => resp.json())
                    .then(data => {
                        if (data.msg) {
                            setStore({
                                error: data
                            })
                        } else {
                            setStore({
                                users: data
                            })
                        }
                    })
            }
        }
    }
}

export default getState;