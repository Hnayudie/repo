import java.util.Date

data class Measurement<T>(
    val timestamp: Date,
    val measurement: T
)
