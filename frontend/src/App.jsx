import FragranceCard from './FragranceCard'
import './App.css'

function App() {
  const fragrances = [
    { name : "Sauvage",brand : "Dior", accords : "Citrus, Woody, Spicy" },
    { name : "Bleu de Chanel", brand : "Chanel", accords : "Citrus, Woody, Aromatic" },
    { name : "Kaaf", brand : "Ahmed Al Maghribi", accords : "Citrus, Woody, Aromatic" },
  ]

  return (
    <>
      <h1>FragBro</h1>
      <p>Catalog</p>
      {fragrances.map(frag => (
        <FragranceCard key={frag.name} frag={frag} />
      ))}
    </>
  )
}

export default App