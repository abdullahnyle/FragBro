import FragranceCard from './FragranceCard'
import './App.css'

function App(){
  return(
    <>
    <h1>FragBro</h1>
    <p>Catalog</p>
    <FragranceCard frag={{ name: "Sauvage", brand: "Dior", accords: "fresh, ambroxan, citrus"}} />
 </>
  )
}
 export default App