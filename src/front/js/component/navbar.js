import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";

export const Navbar = () => {
	const navigate = useNavigate()
	const {actions} = useContext(Context)
	const token= localStorage.getItem("token")
	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">React Boilerplate</span>
				</Link>
				<div className="ml-auto">
					
					{token && <button className="btn btn-danger" onClick={()=>{
						if (actions.makeLogout()) {
							navigate("/")
						}
					}}>Log Out</button>}
					
				</div>
			</div>
		</nav>
	);
};
