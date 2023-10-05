const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			token: "",
			demo: [
				{
					title: "FIRST",
					background: "white",
					initial: "white"
				},
				{
					title: "SECOND",
					background: "white",
					initial: "white"
				}
			]
		},
		actions: {
			// Use getActions to call a function within a fuction
			exampleFunction: () => {
				getActions().changeColor(0, "green");
			},

			getMessage: async () => {
				try{
					// fetching data from the backend
					const resp = await fetch(process.env.BACKEND_URL + "/api/hello")
					const data = await resp.json()
					setStore({ message: data.message })
					// don't forget to return something, that is how the async resolves
					return data;
				}catch(error){
					console.log("Error loading message from backend", error)
				}
			},
			changeColor: (index, color) => {
				//get the store
				const store = getStore();

				//we have to loop the entire demo array to look for the respective index
				//and change its color
				const demo = store.demo.map((elm, i) => {
					if (i === index) elm.background = color;
					return elm;
				});

				//reset the global store
				setStore({ demo: demo });
			},
			makeLogin: async (data) => {
				try {
					const response = await fetch(process.env.BACKEND_URL + "/api/login", {
						method: "POST",
						body: JSON.stringify(data),
						headers: {
							"Content-Type": "application/json"
						}
					})
					const body = await response.json()
					
					if (response.status == 400){
						alert(body.message)
						return false
					} else if (response.status == 404){
						alert(body.message)
						return false
					} else if(response.ok){
						const token = body.token
						setStore({token: token})
						localStorage.setItem("token", token)
						return true
					}
					
				}catch (error) {
					console.log(error)
				}
			},
			makeSignup: async (data) => {
				try {
					const response = await fetch(process.env.BACKEND_URL + "/api/signup", {
						method: "POST",
						body: JSON.stringify(data),
						headers: {
							"Content-Type": "application/json"
						}
					})
					const body = await response.json()
					
					if (response.status == 400){
						alert(body.message)
						return false
					} else if (response.status == 404){
						alert(body.message)
						return false
					} else if(response.ok){
						alert(body.message)
						return true
					}
					
				}catch (error) {
					console.log(error)
				}
			},

			makeLogout: () => {
				localStorage.removeItem("token")
				setStore({token: ""})
				return true
			}

		}
	};
};

export default getState;
