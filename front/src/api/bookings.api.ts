import axios from "axios";

/**
 * Get booking details from API
 */
export const apiBookingDetails = (bookingReference: string) => {
    return axios.get(`/bookings/${encodeURIComponent(bookingReference)}`)
}

/**
 * Get booking checkout lines from API
 */
// [D3] Le front n'envoie plus l'identifiant de session Stripe : le backend le lit en base
export const apiBookingCheckoutLines = (bookingReference: string) => {
    return axios.get(`/bookings/${encodeURIComponent(bookingReference)}/checkout-lines`)
}

/**
 * Register a new booking
 */
export const apiBookingNew = (roomId: string, arrivalDate: string, departureDate: string, guestsCount: number) => {
    return axios.post(`/bookings/`, { roomId, arrivalDate, departureDate, guestsCount })
}

/**
 * Confirm checkout payment of a new booking
 */
export const apiBookingConfirm = (bookingReference: string, confirmationSecret: string) => {
    return axios.post(`/bookings/${encodeURIComponent(bookingReference)}/confirm-checkout`, { confirmationSecret })
}
