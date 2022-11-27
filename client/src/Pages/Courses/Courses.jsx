import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import AddCourseButton from "../../Components/AddCourseButton/AddCourseButton";
import { LoggedUserContext } from "../../Context/LoggedUser";
import ManageAllCourses from "./ManageAllCourses/ManageAllCourses";
import ManageGarantedCourses from "./ManageGarantedCourses/ManageGarantedCourses";
import MyCourses from "./MyCourses/MyCourses";


const Courses = () => {
    const {loggedUser, setLoggedUser} = useContext(LoggedUserContext)
    const [isLoggedIn, setIsLoggedIn] = useState(!!loggedUser.token)

    const navigate = useNavigate();

    useEffect(() => {
        if (!loggedUser.role) navigate('/login')
    }, [loggedUser])

    if (loggedUser.role === 'a')
    return (<ManageAllCourses/>)

    if (loggedUser.role === 'g')
    return (<ManageGarantedCourses/>)

    if (loggedUser.role === 's')
    return (<MyCourses/>)
}

export default Courses