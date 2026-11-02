
function AvailabilityBadge({ available }) {
    return (
        <span className={available > 0 ? 'available' : 'unavailable'}>
            {available > 0 ? 'Available' : 'Unavailable'}
        </span>
    )
}

export default AvailabilityBadge
