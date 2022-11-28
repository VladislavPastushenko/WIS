import './TerminsTable.scss'
import Table from 'react-bootstrap/Table';
import { useContext, useEffect, useState } from 'react';
import createRequest from '../../Services/CreateRequest';
import LoadingIcon from '../LoadingIcon/LoadingIcon';
import { LoggedUserContext } from '../../Context/LoggedUser';
import EditTerminModal from '../EditTeminModal/EditTerminModal';

function TerminsTable({termins=[], repeated=false, onChangeSideEffect}) {
    const {loggedUser, setLoggedUser} = useContext(LoggedUserContext)
    const [terminToEdit, setTerminToEdit] = useState({})
    const [isModalEditOpened, setIsModalEditOpened] = useState(false)

    const editTermin = (termin) => {
        setTerminToEdit(termin);
        setIsModalEditOpened(true)
    }
    return (
        <>
        <div align='center'>
            <div className='terminsTableContainer'>
                <Table bordered>
                    <thead className='bg-info'>
                        <tr>
                            <th style={{width: '50px'}}>Name</th>
                            <th style={{width: '200px'}}>Description</th>
                            <th style={{width: '110px'}}>Time</th>
                            {repeated && <th style={{width: '50px'}}>Weekday</th>}
                            {!repeated && <th style={{width: '75px'}}>Date</th>}
                            <th style={{width: '60px'}}>Max-points</th>
                            {(loggedUser.role === 'a' || loggedUser.role === 'g') && <th style={{width: '50px'}}></th>}
                            {(loggedUser.role === 'a' || loggedUser.role === 'g') && <th style={{width: '50px'}}></th>}
                            {(loggedUser.role === 's') && <th style={{width: '50px'}}>Obtained points</th>}
                        </tr>
                    </thead>
                    <tbody>
                            {termins.map((el, idx) => (
                                    <tr key={el.name}>
                                        <td>{el.name}</td>
                                        <td>{el.description}</td>
                                        <td>{el.time_start} - {el.time_end}</td>
                                        {repeated && <td>{el.weekday}</td>}
                                        {!repeated && <td>{el.date}</td>}
                                        <td>{el.max_points}</td>
                                        {(loggedUser.role === 'a' || loggedUser.role === 'g') && <td><a href="#" onClick={() => {editTermin(el)}}> Edit</a></td>}
                                        {(loggedUser.role === 'a' || loggedUser.role === 'g') && <td><a href={"/termins-users/" + el.id_termin}>Users</a></td>}
                                        {(loggedUser.role === 's') && <th style={{width: '50px'}}> 0 </th>}
                                    </tr>
                                ))
                            }
                    </tbody>
                </Table>
                <EditTerminModal isModalOpen={isModalEditOpened} setModalOpen={setIsModalEditOpened} sideEffectOnChange={onChangeSideEffect} termin={terminToEdit}/>
            </div>
        </div>
        </>
    );
}

export default TerminsTable;