import { useEffect, useState } from 'react'
import LoadingIcon from '../../Components/LoadingIcon/LoadingIcon';
import createRequest from '../../Services/CreateRequest';
import Table from 'react-bootstrap/Table';
import './UserList.scss'
import EditUserModal from '../../Components/EditUserModal/EditUserModal';

const UserList = () => {
    const [users, setUsers] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [userToEdit, setUserToEdit] = useState({})
    const [modalOpen, setModalOpen] = useState(false)

    const downloadUsers = () => {
        setIsLoading(true);

        createRequest({
            path: '/get-all-users',
            method: 'GET'
        })
        .then(res => res.json())
        .then(res => {
            console.log(res)
            setIsLoading(false)
            setUsers(res)
        })
        .catch(err => {
            console.error(err)
            setIsLoading(false)
        })
    }

    useEffect(() => {
        downloadUsers()
    }, [])

    const editUserModalOpen = (user) => {
        setUserToEdit(user)
        setModalOpen(true)
    }
    const onEditUser = (editedUser) => {
        setUsers(prev => {
            return prev.map(el => el.id_person === userToEdit.id_person ? editedUser : el)
        })
    }

    return (
        <div>
            <h2>
                User List
            </h2>
            <div align='center'>
            <div className='usersTableContainer'>
                <Table bordered>
                    <thead className='bg-info'>
                        <tr>
                            <th style={{width: '50px'}}>ID</th>
                            <th>First name</th>
                            <th>Last name</th>
                            <th>Role</th>
                            <th style={{width: '50px'}}></th>
                        </tr>
                    </thead>
                    <tbody>
                        {isLoading ?
                            <tr>
                                <td colSpan={5} className={'text-center'}><LoadingIcon/></td>
                            </tr>
                            :
                            users.map((el, idx) => {
                                return (
                                    <tr key={el.id_person}>
                                        <td>{el.id_person}</td>
                                        <td>{el.firstname}</td>
                                        <td>{el.surname}</td>
                                        <td>{el.role}</td>
                                        <td><a href='#' onClick={() => {editUserModalOpen(el)}}>Edit</a></td>
                                    </tr>
                                )
                            })
                        }
                    </tbody>
                </Table>

                <EditUserModal isModalOpen={modalOpen} setModalOpen={setModalOpen} user={userToEdit} sideEffectOnChange={onEditUser}/>
            </div>
        </div>
        </div>
    )
}
export default UserList