import {useState} from "react"
import axios from "axios"
import { Container, Row, Col} from "react-bootstrap"

export default function Watchlist() {
    const [ticker,setTicker] = useState('')
    const [result,setResult] = useState(null)
    const [error, setError] = useState(false)

    const handleRequest = async () => {
        try {
            const res = await axios.post('http://ec2-54-173-88-96.compute-1.amazonaws.com:5000/get_ticker_sentiment',{ticker})
            setResult(res.data.result)
            setError(false)
        }
        catch (error) {
            console.error('There was an error sending the data', error)
            setError(true)
        }
    }
    return (
        <Container>
            <Row>
                <Col>
                    <h1>Enter a stock ticker to get it&rsquo;s analysis</h1>
                    <input type="text" placeholder="Ex. NVDA" value={ticker} onChange={(e) => setTicker(e.target.value)}/>
                    <button onClick={handleRequest}>Get Analysis!</button>
                    {result !== null && error === false && (<p>Result: {result.toFixed(4)}</p>)}
                    {error && (<p>Error: Unable to retrieve data</p>)}
                </Col>
            </Row>
        </Container>
    );
}