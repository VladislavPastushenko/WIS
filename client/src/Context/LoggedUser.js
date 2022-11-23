import React from "react";

export const loggedUser = {
    token: localStorage.getItem('token')
};

export const LoggedUserContext = React.createContext();