import { useContext, useEffect, useState } from 'react'
import { LoggedUserContext } from '../../Context/LoggedUser'
import './MyProfile.scss'
import { redirect } from "react-router-dom";
import LoadingIcon from '../../Components/LoadingIcon/LoadingIcon';
const MyProfile = () => {
    const {loggedUser, setLoggedUser} = useContext(LoggedUserContext)
    useEffect(() => {
        if (!loggedUser.token)
            redirect('login')

    }, [loggedUser])

    if (!loggedUser.user_id)
    return (
        <div className='text-center'>
            <LoadingIcon/>
        </div>
    )
    else return (
        <div className='text-center'>
            {loggedUser.email}
        </div>
    )
}
export default MyProfile