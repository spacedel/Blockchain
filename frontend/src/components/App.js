import logo from '../assets/coin.gif'
import React, {useState,  useEffect} from "react";
import { API_BASE_URL } from '../config'
import Blockchain from "./Blockchain";

function App() {

  // const [userQuery, setUserQuery] = useState('');
  
  // // setUserQuery value within the state to the value in the event object that repr what user typed.
  // const updateUserQuery = event => {
  //   console.log('userQuery:', userQuery)
  //   setUserQuery(event.target.value);
  // }

  // const searchQuery = () =>{
  //   window.open(`http://google.com/search?q=${userQuery}`);
  // }

  // const handleKeyPress = (event) => {
  //   if (event.key === 'Enter') {
  //     searchQuery();
  //   }
  // } 

  const [walletInfo, setWalletInfo] = useState({});

  // Fetch end point with response as its value then json object of that same value. Empty array allows the useEffect to start once.
  useEffect(() => {
    fetch(`${API_BASE_URL}/wallet/info`)
      .then(response => response.json())
      .then(json => setWalletInfo(json));
  }, []);

  const {address, balance} = walletInfo;

  

  return (
    <div className="App">
      <img className='Logo' src={logo} alt='app-logo'/>
      {/* <div className='coin'></div> */}
      <h3>CAPSULE COIN NETWORK</h3>
      <br />
      <div className='WalletInfo'>
        <div>Address: {address}</div>
        <div>Balance: {balance} CPSL</div>
      </div>
      <br />
      <Blockchain />

      {/* Whatever user types is the input value, changes to updateUserQuery which is an event object */}
      {/* <input value={userQuery} onChange={updateUserQuery} onKeyPress={handleKeyPress} />
      <button onClick={searchQuery}>Search...</button> */}
    </div>
  );
}

export default App;
