import { useContext, useEffect, useState } from 'react'
import { LoggedUserContext } from '../../Context/LoggedUser'
import './MyProfile.scss'
import { redirect } from "react-router-dom";
import LoadingIcon from '../../Components/LoadingIcon/LoadingIcon';
import Button from 'react-bootstrap/Button';
import EditUserModal from '../../Components/EditUserModal/EditUserModal';

const MyProfile = () => {
    const {loggedUser, setLoggedUser} = useContext(LoggedUserContext)
    const [modalOpen, setModalOpen] = useState(false)
    useEffect(() => {
        if (!loggedUser.token)
            redirect('login')

    }, [loggedUser])

    let role;

    switch(loggedUser.role) {
        case 's':
            role = 'Student';
            break;
        case 'g':
            role = 'Garant';
            break;
        case 'a':
            role = 'Administrator';
            break;
        case 'l':
            role = 'Lector';
            break;
        default:
            role = 'Not set';
    }

    if (!loggedUser.user_id)
    return (
        <div className='text-center'>
            <LoadingIcon/>
        </div>
    )
    else return (
        <div>
            <h2>
                My Profile
            </h2>
            <p>
                <span className='fw-bold'>Username</span> - {loggedUser.username || 'Not set'}
            </p>
            <p>
                <span className='fw-bold'>Email</span> - {loggedUser.email || 'Not set'}
            </p>
            <p>
                <span className='fw-bold'>First name</span> - {loggedUser.firstname || 'Not set'}
            </p>
            <p>
                <span className='fw-bold'>Last name</span> - {loggedUser.surname || 'Not set'}
            </p>
            <p>
                <span className='fw-bold'>Address</span> - {loggedUser.address || 'Not set'}
            </p>
            <p>
                <span className='fw-bold'>Phone number</span> - {loggedUser.telephone || 'Not set'}
            </p>
            <p>
                <span className='fw-bold'>Role</span> - {role}
            </p>
            <Button onClick={() => {setModalOpen(true)}}>
                Edit data
            </Button>
            <EditUserModal isModalOpen={modalOpen} setModalOpen={setModalOpen} user={loggedUser} isEditingLoggedUser={true}/>
        </div>
    )
}
export default MyProfile