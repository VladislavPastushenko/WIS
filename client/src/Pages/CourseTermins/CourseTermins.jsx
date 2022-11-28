import { useContext, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import LoadingIcon from '../../Components/LoadingIcon/LoadingIcon';
import TerminsTable from '../../Components/TerminsTable/TerminsTable';
import Button from 'react-bootstrap/Button';
import createRequest from '../../Services/CreateRequest';
import './CourseTermins.scss'
import { LoggedUserContext } from '../../Context/LoggedUser';
import AddTerminModal from '../../Components/AddTerminModal/AddTerminModal';

const CourseTermins = () => {
    const {id} = useParams();
    const [termins, setTermins] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const {loggedUser, setLoggedUser} = useContext(LoggedUserContext)
    const [addTerminModalOpened, setAddTerminModalOpened] = useState(false)

    useEffect(()=> {
        setIsLoading(true);

        createRequest({
            path: '/get-termins-by-course-id/' + id,
            method: 'GET'
        })
        .then(res => res.json())
        .then(res => {
            console.log(res)
            setIsLoading(false)
            setTermins(res)
        })
        .catch(err => {
            console.error(err)
            setIsLoading(false)
        })
    }, [])

    const onAddTermin = (newTermin) => {
        setTermins(prev => [...prev, newTermin])
    }
    return(
        <>
            {isLoading ?
            <div className='text-center'>
                <LoadingIcon/>
            </div>
            :
            <>
                <h4>Lectures</h4>
                <TerminsTable termins={termins.filter(el => el.repeted)} repeated/>
                <h4>Other</h4>
                <TerminsTable termins={termins.filter(el => !el.repeted)}/>
                {(loggedUser.role === 'a' || loggedUser.role === 'g') &&
                    <>
                        <Button onClick={() => {setAddTerminModalOpened(true)}}> Add termin </Button>
                        <AddTerminModal setModalOpen={setAddTerminModalOpened} isModalOpen={addTerminModalOpened} sideEffectOnChange={onAddTermin}/>
                    </>
                }
            </>}

        </>
    )
}

export default CourseTermins