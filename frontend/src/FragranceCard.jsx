function FragranceCard(props){
    const frag = props.frag

    return (
        <div className="frag-card">
        <div className="frag-name">{frag.name}</div>
        <div className="frag-brand">{frag.brand}</div>
        <div className="frag-accords">{frag.accords}</div>
        </div>
    )
}

export default FragranceCard